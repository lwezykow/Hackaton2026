import pandas as pd
import numpy as np

from rules.RuleBase import RuleBase
from rules.RuleDescriptor import RuleDescriptor

class Rule7 (RuleBase):

    TRANSACTIONS_THRESHOLD = 5

    ruleDescriptor = RuleDescriptor(
            rule_id='R7',
            rule_category='Velocity',
            rule='High frequency of transfers',
            business_description='Multiple payments in short time suggest compromise or panic.',
            is_mandatory=True,
            severity=2, # strong
            weight=10,
            difficulty=1 # easy
        )
    
    def __init__(self):
        super().__init__(self.ruleDescriptor) 

    def evaluate(self, df:pd.DataFrame) -> pd.DataFrame :

        df["transaction_timestamp"] = pd.to_datetime(df["transaction_timestamp"])
        df = df.sort_values(["customer_id", "transaction_timestamp"]).reset_index(drop=True).copy()

        df["tx_count_10min"] = (
            df
                .groupby("customer_id")
                .rolling("10min", on="transaction_timestamp")["transaction_id"]
                .count()
                .reset_index(drop=True)
        )
        # df['flag'] = df["tx_count_10min"] >= self.TRANSACTIONS_THRESHOLD
        # df.to_csv('r7_debug.xlsx', index=False)
        # good test evidence on acc = PL394389343608791669579040

        df_filtered = df[df["tx_count_10min"] >= self.TRANSACTIONS_THRESHOLD]        

        result = pd.DataFrame()

        result['transaction_id'] = df_filtered[['transaction_id']]
        result['rule_id'] = self.ruleDescriptor.rule_id
        result['severity'] = self.ruleDescriptor.severity
        result['weight'] = self.ruleDescriptor.weight
        result['remarks'] = f"High frequency of transfers detected, {self.TRANSACTIONS_THRESHOLD} or more"

        return result