import pandas as pd

from rules.RuleBase import RuleBase
from rules.RuleDescriptor import RuleDescriptor
from utils.Normalizer import Normalizer

class Rule8 (RuleBase):
   
           
    ruleDescriptor = RuleDescriptor(
            rule_id='R8',
            rule_category='Velocity',
            rule='New payees burst',
            business_description='Many new beneficiaries added in short period, indicative of mule activity.',
            is_mandatory=False,
            severity=1,
            weight=8,
            difficulty=2
        )
    
    def __init__(self):
        super().__init__(self.ruleDescriptor) 

    def evaluate(self, df:pd.DataFrame) -> pd.DataFrame :
        
        df["transaction_timestamp"] = pd.to_datetime(df["transaction_timestamp"])

        df_nb = (
            df[df["is_new_beneficiary"]]
                .sort_values(["customer_id", "transaction_timestamp"])
                .reset_index(drop=True)
        )

        df_nb["cnt_24h"] = (
            df_nb.groupby("customer_id")
                .rolling("24h", on="transaction_timestamp")["transaction_id"]
                .count()
                .reset_index(drop=True)
        )

        df_result = df_nb[df_nb["cnt_24h"] >= 3]

        result = pd.DataFrame()

        result['transaction_id'] = df_result[['transaction_id']]
        result['rule_id'] = self.ruleDescriptor.rule_id
        result['severity'] = self.ruleDescriptor.severity
        result['weight'] = self.ruleDescriptor.weight
        result['remarks'] = f"Payment amount is 3x higer compared to 30-day customer average"                    

        return result
    
