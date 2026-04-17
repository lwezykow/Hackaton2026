import pandas as pd
import pytest

from rules.r24 import Rule24

# if 'pytest' not work for you try following:
# first you need to install few things:
#     pip install pytest
#     pip install .
# then in bash type 'pytest' to exec unit tests
#     pytest

@pytest.mark.parametrize("channel,amount,tx_amount_expected,tx_expected_name", [
    ("Mobile", 1999, 0, None),   
    ("Mobile", 2000, 0, None),   
    ("Mobile", 2001, 1, "TX-000001"), # above threshold

    ("Web", 4999, 0, None),   
    ("Web", 5000, 0, None),   
    ("Web", 5001, 1, "TX-000001"), # above threshold

    ("Phone", 999, 0, None),   
    ("Phone", 1000, 0, None),   
    ("Phone", 1001, 1, "TX-000001"), # above threshold

    ("ATM", 999, 0, None),   
    ("ATM", 1000, 0, None),   
    ("ATM", 1001, 1, "TX-000001"), # above threshold

    ("Branch", 9999, 0, None),   
    ("Branch", 10000, 0, None),   
    ("Branch", 10001, 1, "TX-000001"), # above threshold

    ("Corporate API", 24999, 0, None),   
    ("Corporate API", 25000, 0, None),   
    ("Corporate API", 25001, 1, "TX-000001"), # above threshold
])
def test_r24_evaluate_amount_is_over_15k_EUR_FLAG_as_fraud(channel:str, amount:float, tx_amount_expected:int, tx_expected_name:str):
    rule = Rule24()

    data = [
        {
            "transaction_id": "TX-000001",
            "transaction_timestamp": "2025-12-19T00:00:00+00:00",
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627",
            "channel": channel,                           # inject channel
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": amount,                              # inject amount
            "currency": "EUR",
            "is_new_beneficiary": False,
            "beneficiary_account": "DE358075381662562554536117",
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        }
    ]

    df_input = pd.DataFrame(data)
    df_input["transaction_timestamp"] = pd.to_datetime(df_input["transaction_timestamp"])

    df_output = rule.evaluate(df_input)

    assert len(df_output) == tx_amount_expected
    if tx_amount_expected > 0:
        assert df_output.iloc[0]['transaction_id'] == tx_expected_name
