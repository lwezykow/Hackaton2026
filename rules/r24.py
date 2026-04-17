import pandas as pd

from rules.RuleBase import RuleBase
from rules.RuleDescriptor import RuleDescriptor


class Rule24 (RuleBase):

    CHANNEL_THRESHOLDS = {
        "Mobile": 2000,
        "Web": 5000,
        "Phone": 1000,
        "ATM": 1000,
        "Branch": 10000,
        "Corporate API": 25000,
    }

    ruleDescriptor = RuleDescriptor(
            rule_id='R24',
            rule_category='Threshold',
            rule='Channel-Specific Threshold',
            business_description='Each channel has different safe maximum values.',
            is_mandatory=True,
            severity = 1, # Mild
            weight = 5, 
            difficulty= 1 # Easy
        )
    
    def __init__(self):
        super().__init__(self.ruleDescriptor) 


    def evaluate(self, df:pd.DataFrame) -> pd.DataFrame :
        result = pd.DataFrame()

        for key in self.CHANNEL_THRESHOLDS.keys():
            threshold = self.CHANNEL_THRESHOLDS[key]
            df_filtered = df[(df["channel"] == key) & (df["amount"] > threshold)]

            group_result = pd.DataFrame()
            group_result['transaction_id'] = df_filtered[['transaction_id']]
            group_result['rule_id'] = self.ruleDescriptor.rule_id
            group_result['severity'] = self.ruleDescriptor.severity
            group_result['weight'] = self.ruleDescriptor.weight
            group_result['remarks'] = f'Channel {key} safe maximum value of €{threshold:,} has been exceeded'

            result = pd.concat([result, group_result], ignore_index=True)
        return result
