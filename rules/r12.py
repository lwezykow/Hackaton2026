import numpy as np
import pandas as pd

from rules.RuleBase import RuleBase
from rules.RuleDescriptor import RuleDescriptor


class Rule12 (RuleBase):

    Z_SCORE_THRESHOLD = 3
    ruleDescriptor = RuleDescriptor(
            rule_id='R12',
            rule_category='Anomaly',
            rule='Z-score amount',
            business_description="Payment amount deviates strongly from user's statistical pattern. z-score measures how far the amount is from the customer's usual average. if z-score > 3 means that amount is more than 3 standard deviations above normal → statistically very unusual.",
            is_mandatory=False,
            severity = 2, # Strong
            weight = 12, 
            difficulty= 3 # Hard
        )
    
    def __init__(self):
        super().__init__(self.ruleDescriptor) 


    def evaluate(self, df:pd.DataFrame) -> pd.DataFrame :

        df["amount_mean"] = df.groupby("customer_account")["amount"].transform("mean")
        df["amount_std"] = df.groupby("customer_account")["amount"].transform("std")
        df["amount_zscore"] = (
            (df["amount"] - df["amount_mean"]) / df["amount_std"]
            .replace(0, np.nan)
        ).fillna(0)        
        df["flag"] = df["amount_zscore"] > self.Z_SCORE_THRESHOLD

        #df.to_csv('r12_debug.xlsx', index=False)

        df_filtered = df[df["amount_zscore"] > self.Z_SCORE_THRESHOLD]

        result = pd.DataFrame()
        result['transaction_id'] = df_filtered[['transaction_id']]

        result['rule_id'] = self.ruleDescriptor.rule_id
        result['severity'] = self.ruleDescriptor.severity
        result['weight'] = self.ruleDescriptor.weight
        result['remarks'] = f"Payment amount deviates strongly from user's statistical pattern. z-score is above {self.Z_SCORE_THRESHOLD} threshold"
        return result
