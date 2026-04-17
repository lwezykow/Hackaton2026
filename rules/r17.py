import pandas as pd
import numpy as np

from rules.RuleBase import RuleBase
from rules.RuleDescriptor import RuleDescriptor

class Rule17 (RuleBase):

    MIN_CLIENT_TRANSACTIONS = 5
    LOWER_AMOUNT_BOUNDARY = 13500
    UPPER_AMOUNT_BOUNDARY = 14999

    ruleDescriptor = RuleDescriptor(
            rule_id='R17',
            rule_category='FRAML',
            rule='Smurfing/structuring',
            business_description='Repeated small payments near threshold to avoid detection.',
            is_mandatory=False,
            severity = 2, # ??????
            weight = 15,
            difficulty = 2 # Medium
        )
    
    def __init__(self):
        super().__init__(self.ruleDescriptor) 

    def evaluate(self, df:pd.DataFrame) -> pd.DataFrame :

        df["transaction_timestamp"] = pd.to_datetime(df["transaction_timestamp"])
        df = df.sort_values(["customer_id", "transaction_timestamp"]).reset_index(drop=True).copy()
        df["suspicious_value"] = (
            (df["amount"] >= self.LOWER_AMOUNT_BOUNDARY) &
            (df["amount"] <= self.UPPER_AMOUNT_BOUNDARY)
        ).astype(int)

        rolling = (
            df.groupby("customer_id")
            .rolling("2h", on="transaction_timestamp")
        )

        agg = rolling.agg({
            "transaction_id": "count",
            "suspicious_value": "sum"
        }).reset_index(drop=True)
        
        df["tx_count_2h"] = agg["transaction_id"]
        df["suspicious_value_sum_2h"] = agg["suspicious_value"]

        df['filter'] = (df["suspicious_value_sum_2h"] >= self.MIN_CLIENT_TRANSACTIONS)
        # df.to_csv('r17_debug.xlsx', index=False)
        # good test example - acc PL745139992949457037354436

        df_filtered = df[df["suspicious_value_sum_2h"] >= self.MIN_CLIENT_TRANSACTIONS]

        result = pd.DataFrame()

        result['transaction_id'] = df_filtered[['transaction_id']]
        result['rule_id'] = self.ruleDescriptor.rule_id
        result['severity'] = self.ruleDescriptor.severity
        result['weight'] = self.ruleDescriptor.weight
        result['remarks'] = f"Smurfing detcted - repeated small payments near threshold to avoid detection."

        return result