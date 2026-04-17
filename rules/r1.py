import pandas as pd

from rules.RuleBase import RuleBase
from rules.RuleDescriptor import RuleDescriptor
from utils.Normalizer import Normalizer

class Rule1 (RuleBase):

    SIMILARITY_THRESHOLD = 0.8

    ruleDescriptor = RuleDescriptor(
            rule_id='R1',
            rule_category='Confirmation of Payee (CoP)',
            rule='CoP Name Mismatch - Hard Fail',
            business_description='''The entered beneficiety name is significantly different from the official registered account name, indicating high fraud risk.
For CoP in real the sender's bank sends the entered name + IBAN to the receiving bank's API
The receiving bank  performs comparition with the account owner name and returns results.''',
            is_mandatory=True,
            severity=2,
            weight=25,
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

        df_filtered = df[df["similarity_score"] < self.SIMILARITY_THRESHOLD]

        result = pd.DataFrame()

        result['transaction_id'] = df_filtered[['transaction_id']]
        result['rule_id'] = self.ruleDescriptor.rule_id
        result['severity'] = self.ruleDescriptor.severity
        result['weight'] = self.ruleDescriptor.weight
        result['remarks'] = f"Confirmation of Payee - Name Mismatch detected"

        return result