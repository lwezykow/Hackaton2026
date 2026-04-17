import pandas as pd

from rules.RuleBase import RuleBase
from rules.RuleDescriptor import RuleDescriptor
from utils.Normalizer import Normalizer

class Rule2 (RuleBase):

    LOWER_SIMILARITY_BOUNDRY = 0.8
    UPPER_SIMILARITY_BOUNDRY = 0.89

    ruleDescriptor = RuleDescriptor(
            rule_id='R2',
            rule_category='Confirmation of Payee (CoP)',
            rule='CoP Name Mismatch - Soft Warning',
            business_description='A minor mismatch exists between entered name and official account name, often due to typos but requiring user awareness.',
            is_mandatory=False,
            severity=1,
            weight=5,
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

        df.to_csv('sim_score.csv', index=False)

        df_filtered = df[(df["similarity_score"].between(self.LOWER_SIMILARITY_BOUNDRY, self.UPPER_SIMILARITY_BOUNDRY))]
        
        result = pd.DataFrame()

        result['transaction_id'] = df_filtered[['transaction_id']]
        result['rule_id'] = self.ruleDescriptor.rule_id
        result['severity'] = self.ruleDescriptor.severity
        result['weight'] = self.ruleDescriptor.weight
        result['remarks'] = f"CoP Name Mismatch - Soft Warning"

        return result