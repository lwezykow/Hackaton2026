from datetime import datetime, timedelta
import logging
import random
import sys
import time
from venv import logger
import numpy as np
import pandas as pd
from typing import Optional, cast

from rules.r22 import Rule22

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
print(df_transactions)


df_combined_rules_results = pd.DataFrame()

# ---------------------
# --- run rules
rules = [Rule22()]
for rule in rules:
    rule_start = time.perf_counter()

    df_ruleInput = df_transactions.copy()
    df_rule_result = rule.evaluate(df_ruleInput)
    df_combined_rules_results = pd.concat([df_combined_rules_results, df_rule_result], ignore_index=True) # this can be optimized if slow

    rule_end = time.perf_counter()
    print(f"{rule.ruleDescriptor.rule_id} - execution time: {rule_end - rule_start:.3f} seconds, entries affected: {len(df_rule_result)}")

# ---------------------
# --- process rule ouputs


# ---------------------
# -- aggregate and calculate scores


# ---------------------
# -- prepare classified transactions dataframe keeping only output columns 
df_classified_transactions_output = pd.DataFrame()
df_classified_transactions_output['transaction_id'] = df_transactions['transaction_id']
df_classified_transactions_output['triggered_rules'] = [
    random.choice(['R1','R22','R24','R1;R22','R1;24'])
    for _ in range(len(df_classified_transactions_output))
]
df_classified_transactions_output['is_fraud_transaction'] = [
    random.choice(['True','False'])
    for _ in range(len(df_classified_transactions_output))
]
df_classified_transactions_output['risk_score'] = [
    random.choice([random.random() * 100.0])
    for _ in range(len(df_classified_transactions_output))
]
df_classified_transactions_output['risk_category'] = [
    random.choice(['LOW','MEDIUM','HIGH'])
    for _ in range(len(df_classified_transactions_output))
]

print(df_classified_transactions_output)

# --- save file with transactions fraud classifications
print(f'Saving classified FRAML transactions file: {TX_INPUT_FILE}')
df_classified_transactions_output.to_csv(TX_OUTPUT_FILE, index=False)

end = time.perf_counter()
print(f"Total execution time: {end - start:.3f} seconds")