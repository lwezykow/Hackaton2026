import pandas as pd

from rules.RuleBase import RuleBase
from rules.RuleDescriptor import RuleDescriptor
from utils.Normalizer import Normalizer

class Rule3 (RuleBase):
    
    SIMILARITY_THRESHOLD = 0.89

    ruleDescriptor = RuleDescriptor(
            rule_id='R3',
            rule_category='Confirmation of Payee (CoP)',
            rule='New Beneficiary + CoP Mismatch',
            business_description='Payment to first - time recipient with insufficient name match, increasing fraud likelihood.',
            is_mandatory=False,
            severity=1,
            weight=10,
            difficulty=1
        )
    
    def __init__(self):
        super().__init__(self.ruleDescriptor) 

    def evaluate(self, df:pd.DataFrame) -> pd.DataFrame :

        normalizer = Normalizer()

        df["similarity_score"] = df.apply(
            lambda row: normalizer.get_similarity_score(
                row["entered_beneficiary_name"],
                row["official_beneficiary_account_name"],
            ),
            axis=1
        )
        
        df_filtered = df[((df["similarity_score"] < self.SIMILARITY_THRESHOLD) & (df["is_new_beneficiary"] == True))]               

        result = pd.DataFrame()

        result['transaction_id'] = df_filtered[['transaction_id']]
        result['rule_id'] = self.ruleDescriptor.rule_id
        result['severity'] = self.ruleDescriptor.severity
        result['weight'] = self.ruleDescriptor.weight
        result['remarks'] = f"New Beneficiary + CoP Mismatch"

        return result