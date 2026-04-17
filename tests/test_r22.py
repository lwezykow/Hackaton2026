import pandas as pd
import pytest

from rules.r22 import Rule22

# if 'pytest' not work for you try following:
# first you need to install few things:
#     pip install pytest
#     pip install .
# then in bash type 'pytest' to exec unit tests
#     pytest

def test_r22_evaluate_amount_is_over_15k_EUR_FLAG_as_fraud():
    rule = Rule22()

    data = [
        {
            "transaction_id": "TX-000001",
            "transaction_timestamp": "2025-12-19T00:00:00+00:00",
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627",
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 15001, # above threshold
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
    # ensure we have correctly identified single transaction with amount over threshold
    assert len(df_output) == 1
    assert df_output.loc[0]['transaction_id'] == 'TX-000001' 

def test_r22_evaluate_amount_is_under_15k_EUR_DONT_flag_as_fraud():
    rule = Rule22()

    data = [
        {
            "transaction_id": "TX-000001",
            "transaction_timestamp": "2025-12-19T00:00:00+00:00",
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627",
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 15000, # equal to threshold
            "currency": "EUR",
            "is_new_beneficiary": False,
            "beneficiary_account": "DE358075381662562554536117",
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        },
        {
            "transaction_id": "TX-000002",
            "transaction_timestamp": "2025-12-19T00:00:00+00:00",
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627",
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 14999,  # less than threshold
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
    # ensure we haven't misidentified transactions as fraud
    assert len(df_output) == 0
    
