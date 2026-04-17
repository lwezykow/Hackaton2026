import pandas as pd

from rules.RuleBase import RuleBase
from rules.RuleDescriptor import RuleDescriptor


class Rule22 (RuleBase):

    AMOUNT_THRESHOLD = 15000
    ruleDescriptor = RuleDescriptor(
            rule_id='R22',
            rule_category='Threshold',
            rule='Absolute High-Value Threshold',
            business_description='Payment exceeds predefined limit.',
            is_mandatory=True,
            severity = 2, # Strong
            weight = 10, 
            difficulty= 1 # Easy
        )
    
    def __init__(self):
        super().__init__(self.ruleDescriptor) 


    def evaluate(self, df:pd.DataFrame) -> pd.DataFrame :

        df_filtered = df[df["amount"] > self.AMOUNT_THRESHOLD]

        result = pd.DataFrame()
        result['transaction_id'] = df_filtered[['transaction_id']]

        result['rule_id'] = self.ruleDescriptor.rule_id
        result['severity'] = self.ruleDescriptor.severity
        result['weight'] = self.ruleDescriptor.weight
        result['remarks'] = 'Payment exceeds predefined limit amount of €15,000'
        return result
