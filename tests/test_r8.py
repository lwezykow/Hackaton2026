import pandas as pd
import pytest

from rules.r8 import Rule8

# if 'pytest' not work for you try following:
# first you need to install few things:
#     pip install pytest
#     pip install .
# then in bash type 'pytest' to exec unit tests
#     pytest

def test_r8_two_transactions_should_not_flag_customer_transactions_as_fraud():
    rule = Rule8()

    data = [
        {
            "transaction_id": "TX-000001",
            "transaction_timestamp": "2025-12-19T00:00:00+00:00",
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627", 
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 1000, 
            "currency": "EUR",
            "is_new_beneficiary": True,
            "beneficiary_account": "PL358075381662562554536117",   # we send PL
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        },
        {
            "transaction_id": "TX-000002",
            "transaction_timestamp": "2025-12-19T00:01:00+00:00",   # hr +1
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627",
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 15001,                                  # and amount above threshold
            "currency": "EUR",
            "is_new_beneficiary": True,
            "beneficiary_account": "DE358075381662562554536117",    # and now we send DE
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        }
    ]

    df_input = pd.DataFrame(data)
    df_input["transaction_timestamp"] = pd.to_datetime(df_input["transaction_timestamp"])

    df_output = rule.evaluate(df_input)
    
    assert len(df_output) == 0
    

def test_r8_three_transactions_should_flag_customer_transactions_as_fraud():
    rule = Rule8()

    data = [
        {
            "transaction_id": "TX-000001",
            "transaction_timestamp": "2025-12-19T00:00:00+00:00",
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627", 
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 1000, 
            "currency": "EUR",
            "is_new_beneficiary": True,
            "beneficiary_account": "PL358075381662562554536117",   # we send PL
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        },
        {
            "transaction_id": "TX-000002",
            "transaction_timestamp": "2025-12-19T00:01:00+00:00",   # hr +1
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627",
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 15001,                                  # and amount above threshold
            "currency": "EUR",
            "is_new_beneficiary": True,
            "beneficiary_account": "DE358075381662562554536117",    # and now we send DE
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        },       
        {
            "transaction_id": "TX-000004",
            "transaction_timestamp": "2025-12-19T05:55:00+00:00",
            "customer_id": 2045,
            "customer_account": "PL881208393661999813073093",
            "channel": "Phone",
            "device_id": "PHONE-IVR-1BEFE8F3",
            "amount": 92.38,
            "currency": "EUR",
            "is_new_beneficiary": True,
            "beneficiary_account": "DE036816470235268897123624",
            "entered_beneficiary_name": "Helen Palmer",
            "official_beneficiary_account_name": "Helen Palmer",
            "customer_account_balance": 427798.64
        }
    ]

    df_input = pd.DataFrame(data)
    df_input["transaction_timestamp"] = pd.to_datetime(df_input["transaction_timestamp"])

    df_output = rule.evaluate(df_input)
    
    assert len(df_output) == 1
    assert df_output.iloc[0]['transaction_id'] == 'TX-000004'

def test_r8_three_transactions_should_not_flag_customer_transactions_as_fraud_when_window_is_larger_than_24h():
    rule = Rule8()

    data = [
        {
            "transaction_id": "TX-000001",
            "transaction_timestamp": "2025-12-19T00:00:00+00:00",
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627", 
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 1000, 
            "currency": "EUR",
            "is_new_beneficiary": True,
            "beneficiary_account": "PL358075381662562554536117",   # we send PL
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        },
        {
            "transaction_id": "TX-000002",
            "transaction_timestamp": "2025-12-19T00:01:00+00:00",   # hr +1
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627",
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 15001,                                  # and amount above threshold
            "currency": "EUR",
            "is_new_beneficiary": True,
            "beneficiary_account": "DE358075381662562554536117",    # and now we send DE
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        },       
        {
            "transaction_id": "TX-000004",
            "transaction_timestamp": "2025-12-21T05:55:00+00:00",
            "customer_id": 2045,
            "customer_account": "PL881208393661999813073093",
            "channel": "Phone",
            "device_id": "PHONE-IVR-1BEFE8F3",
            "amount": 92.38,
            "currency": "EUR",
            "is_new_beneficiary": True,
            "beneficiary_account": "DE036816470235268897123624",
            "entered_beneficiary_name": "Helen Palmer",
            "official_beneficiary_account_name": "Helen Palmer",
            "customer_account_balance": 427798.64
        }
    ]

    df_input = pd.DataFrame(data)
    df_input["transaction_timestamp"] = pd.to_datetime(df_input["transaction_timestamp"])

    df_output = rule.evaluate(df_input)
    
    assert len(df_output) == 0    