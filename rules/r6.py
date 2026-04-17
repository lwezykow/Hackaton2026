import pandas as pd

from rules.RuleBase import RuleBase
from rules.RuleDescriptor import RuleDescriptor
from utils.Normalizer import Normalizer

class Rule6 (RuleBase):
    
    STRONG_MULTIPLICATION_FACTOR = 10
    MILD_MULTIPLICATION_FACTOR = 3
    SEVERITY_ADDON = 1
        
    ruleDescriptor = RuleDescriptor(
            rule_id='R6',
            rule_category='Velocity',
            rule='High amount spike',
            business_description='Payment amount is unusually high compared to 30-day customer average.',
            is_mandatory=False,
            severity=1,
            weight=8,
            difficulty=2
        )
    
    def __init__(self):
        super().__init__(self.ruleDescriptor) 

    def evaluate(self, df:pd.DataFrame) -> pd.DataFrame :
        
        df["transaction_timestamp"] = pd.to_datetime(df["transaction_timestamp"])

        df = (
            df.sort_values(["customer_id", "transaction_timestamp"])
            .reset_index(drop=True)
            .copy()
        )

        df["avg_amount_30d"] = (
            df.groupby("customer_id")
            .rolling("30D", on="transaction_timestamp")["amount"]
            .mean()
            .reset_index(drop=True)
        )

        df_10x_above_avg = df[(df["amount"] > df["avg_amount_30d"] * self.STRONG_MULTIPLICATION_FACTOR)]
                
        result_10x = pd.DataFrame()

        result_10x['transaction_id'] = df_10x_above_avg[['transaction_id']]
        result_10x['rule_id'] = self.ruleDescriptor.rule_id
        result_10x['severity'] = self.ruleDescriptor.severity + self.SEVERITY_ADDON
        result_10x['weight'] = self.ruleDescriptor.weight
        result_10x['remarks'] = f"Payment amount is 10x higer compared to 30-day customer average"

        df_3x_above_avg = df[(df["amount"] > df["avg_amount_30d"] * self.MILD_MULTIPLICATION_FACTOR) & (df["amount"] <= df["avg_amount_30d"] * self.STRONG_MULTIPLICATION_FACTOR)]
        
        result_3x = pd.DataFrame()

        result_3x['transaction_id'] = df_3x_above_avg[['transaction_id']]
        result_3x['rule_id'] = self.ruleDescriptor.rule_id
        result_3x['severity'] = self.ruleDescriptor.severity
        result_3x['weight'] = self.ruleDescriptor.weight
        result_3x['remarks'] = f"Payment amount is 3x higer compared to 30-day customer average"             

        df_union = pd.concat([result_10x, result_3x], axis=0, ignore_index=True)               

        return df_union
    
