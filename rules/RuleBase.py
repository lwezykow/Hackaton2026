
import pandas as pd

from rules.RuleDescriptor import RuleDescriptor


class RuleBase:

    def __init__(self, ruleDescriptor: RuleDescriptor):
        self.ruleDescriptor = ruleDescriptor

    def get_descriptor(self) -> RuleDescriptor:
        return self.ruleDescriptor

    def evaluate(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame()
    