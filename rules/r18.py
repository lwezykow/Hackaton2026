import pandas as pd
import numpy as np

from rules.RuleBase import RuleBase
from rules.RuleDescriptor import RuleDescriptor

class Rule18 (RuleBase):

    MAX_CLIENT_TRANSACTIONS = 3

    ruleDescriptor = RuleDescriptor(
            rule_id='R18',
            rule_category='FRAML',
            rule='Round amounts anomaly',
            business_description='Multiple round-number payments indicative of scam instructions.',
            is_mandatory=True,
            severity=2,
            weight=3,
            difficulty=1
        )
    
    def __init__(self):
        super().__init__(self.ruleDescriptor) 

    def evaluate(self, df:pd.DataFrame) -> pd.DataFrame :

        df_filtered = df[np.isclose(df["amount"] % 10, 0)]
        df_filtered = df_filtered.copy()
        df_filtered["transaction_timestamp"] = pd.to_datetime(df_filtered["transaction_timestamp"])
        df_filtered = df_filtered.sort_values(["customer_id", "transaction_timestamp"]).reset_index(drop=True).copy()

        df_filtered["tx_count_48h"] = (
            df_filtered
                .groupby("customer_id")
                .rolling("48h", on="transaction_timestamp")["transaction_id"]
                .count()
                .reset_index(drop=True)
        )
        
        df_filtered['filter'] = (df_filtered["tx_count_48h"] >= self.MAX_CLIENT_TRANSACTIONS)
        #df.to_csv('r18_debug.xlsx', index=False)
        df_filtered = df_filtered[df_filtered["tx_count_48h"] >= self.MAX_CLIENT_TRANSACTIONS]        

        result = pd.DataFrame()

        result['transaction_id'] = df_filtered[['transaction_id']]
        result['rule_id'] = self.ruleDescriptor.rule_id
        result['severity'] = self.ruleDescriptor.severity
        result['weight'] = self.ruleDescriptor.weight
        result['remarks'] = f"Round amounts anomaly detected"

        return result