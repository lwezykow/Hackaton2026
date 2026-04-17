from datetime import datetime, timedelta
from typing import Dict
import logging
import random
import sys
import time
from venv import logger
import numpy as np
import pandas as pd
from typing import Optional, cast

from rules.r1 import Rule1
from rules.r2 import Rule2
from rules.r3 import Rule3
from rules.r7 import Rule7
from rules.r10 import Rule10
from rules.r18 import Rule18
from rules.r12 import Rule12
from rules.r22 import Rule22
from rules.r24 import Rule24

FRAUD_THRESHOLD = 30

#-- setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TX_INPUT_FILE = './data/inputs.csv'
TX_OUTPUT_FILE = './data/outputs.csv'

start = time.perf_counter()
# ---------------------
# --- load file with transactions to data frame
print(f'Loading transactions file: {TX_INPUT_FILE}')
df_transactions = pd.read_csv(TX_INPUT_FILE)
print('Input transactions sample:')
print(df_transactions)


df_combined_rules_results = pd.DataFrame()

# ---------------------
# --- run rules
rules = [
    Rule1(),
    Rule2(),
    Rule3(),
    Rule7(),
    Rule10(),
    Rule18(),
    Rule12(),
    Rule22(),
    Rule24(),
    ]
for rule in rules:
    rule_start = time.perf_counter()

    df_ruleInput = df_transactions.copy()
    df_rule_result = rule.evaluate(df_ruleInput)
    df_combined_rules_results = pd.concat([df_combined_rules_results, df_rule_result], ignore_index=True) # this can be optimized if slow

    rule_end = time.perf_counter()
    print(f"{rule.ruleDescriptor.rule_id} - execution time: {rule_end - rule_start:.3f} seconds, entries affected: {len(df_rule_result)}")

# ---------------------
# --- process rule ouputs
print('Combined rules sample:')
print(df_combined_rules_results)

# calculate raw scores per each rule separately
df_combined_rules_results['raw_score'] = df_combined_rules_results['severity'] * df_combined_rules_results['weight']

# aggregate raw scores to transaction level
df_combined_rules_results_grouped = (
    df_combined_rules_results
    .groupby("transaction_id", as_index=False)["raw_score"]
    .sum()
)

# merge aggregates to input set of transactions
df_classified_transactions = pd.DataFrame()
df_classified_transactions['transaction_id'] = df_transactions['transaction_id']
df_classified_transactions = df_classified_transactions.merge(df_combined_rules_results_grouped, how="left", on="transaction_id")
df_classified_transactions.fillna(0, inplace=True)


# clip aggregated raw score to 0-100 range to produce risk score
df_classified_transactions["risk_score"] = df_classified_transactions["raw_score"].clip(lower=0, upper=100)

# depending on risk score threshold assign risk category
df_classified_transactions["risk_category"] = np.select(
    [df_classified_transactions["risk_score"] < 30,
    (df_classified_transactions["risk_score"] >= 30) & (df_classified_transactions["risk_score"] < 70),
    df_classified_transactions["risk_score"] >= 70],
    ["LOW", "MEDIUM", "HIGH"],
    default="UNKNOWN"
)

# set flag whether transaction is fraud or not deciding if risk score has surpased fraud threshold
df_classified_transactions["is_fraud_transaction"] = (
    df_classified_transactions["risk_score"] >= FRAUD_THRESHOLD
)

# note which rules were source of risk score  
df_grouped_ruleIds = df_combined_rules_results.groupby("transaction_id", as_index=False)["rule_id"].agg(";".join)
df_grouped_ruleIds.rename(columns={"rule_id": "triggered_rules"}, inplace=True)
df_classified_transactions = df_classified_transactions.merge(df_grouped_ruleIds, how="left", on="transaction_id")
df_classified_transactions.fillna('', inplace=True)


# ---------------------
# --- save file with transactions fraud classifications
print('Output file sample:')
df_classified_transactions_output = df_classified_transactions[['transaction_id','triggered_rules','is_fraud_transaction','risk_score','risk_category']]
print(df_classified_transactions)

print(f'Saving classified FRAML transactions file: {TX_INPUT_FILE}')
df_classified_transactions_output.to_csv(TX_OUTPUT_FILE, index=False)

end = time.perf_counter()
print(f"Total execution time: {end - start:.3f} seconds")