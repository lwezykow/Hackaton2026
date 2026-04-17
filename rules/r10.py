import pandas as pd

from rules.RuleBase import RuleBase
from rules.RuleDescriptor import RuleDescriptor


class Rule10 (RuleBase):

    AMOUNT_THRESHOLD = 15000
    ruleDescriptor = RuleDescriptor(
            rule_id='R10',
            rule_category='Anomaly',
            rule='Cross-border anomaly',
            business_description='Payment sent to sudden, never-before-seen country signals unusual behaviour.',
            is_mandatory=False,
            severity = 1, # Mild
            weight = 8, 
            difficulty = 2 # Medium
        )
    
    def __init__(self):
        super().__init__(self.ruleDescriptor) 


    def evaluate(self, df:pd.DataFrame) -> pd.DataFrame :

        df["transaction_timestamp"] = pd.to_datetime(df["transaction_timestamp"])
        df = df.sort_values(["customer_id", "transaction_timestamp"]).reset_index(drop=True).copy()

        # make country column from IBANs
        df["country_code"] = df["beneficiary_account"].str[:2]

        # map previous transaction
        df[["prev_transaction_id","prev_country_code","prev_transaction_timestamp"]] = (
            df.groupby("customer_id")[["transaction_id","country_code","transaction_timestamp"]].shift(1)
        )
        df.fillna('', inplace=True)

        # make list of country_codes as an array 
        df["country_code_list"] = (
            df.groupby("customer_id")["country_code"]
            .transform(lambda x: [
                list(dict.fromkeys(x.iloc[:i+1]))  # keeps order + distinct
                for i in range(len(x))
            ])
        )
        
        df["country_code_list"] = (
            df.groupby("customer_id")["country_code_list"].shift(1)
        )

        df["is_new_country"] = ~df.apply(
            lambda row: row["country_code"] in row["country_code_list"]
            if isinstance(row["country_code_list"], list) else False,
            axis=1
        )

        # print(df)
        #df.to_csv('r10_debug.xlsx', index=False)
        
        df_filtered = df[(df["is_new_country"] == True) & (df["amount"] > self.AMOUNT_THRESHOLD)]
        df_filtered.to_csv('r10_debug.xlsx', index=False)

        result = pd.DataFrame()
        result['transaction_id'] = df_filtered[['transaction_id']]

        result['rule_id'] = self.ruleDescriptor.rule_id
        result['severity'] = self.ruleDescriptor.severity
        result['weight'] = self.ruleDescriptor.weight
        result['remarks'] = f'Payment exceeds predefined limit amount of €{self.AMOUNT_THRESHOLD:,} and sent to sudden, never-before-seen country.'
        
        #print(result)
        return result
