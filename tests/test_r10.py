import pandas as pd
import pytest

from rules.r10 import Rule10

# if 'pytest' not work for you try following:
# first you need to install few things:
#     pip install pytest
#     pip install .
# then in bash type 'pytest' to exec unit tests
#     pytest

def test_r10_evaluate_amount_is_over_15k_EUR_and_new_country_code_spotted_FLAG_as_fraud():
    rule = Rule10()

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
            "is_new_beneficiary": False,
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
            "is_new_beneficiary": False,
            "beneficiary_account": "DE358075381662562554536117",    # and now we send DE
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        }
    ]

    df_input = pd.DataFrame(data)
    df_input["transaction_timestamp"] = pd.to_datetime(df_input["transaction_timestamp"])

    df_output = rule.evaluate(df_input)
    # ensure we have correctly identified transaction TX-000002 with amount over threshold and new country code
    assert len(df_output) == 1
    assert df_output.iloc[0]['transaction_id'] == 'TX-000002' 

def test_r10_evaluate_amount_is_over_15k_EUR_and_new_country_code_spotted_FLAG_as_fraud___case2():
    rule = Rule10()

    data = [
        {
            "transaction_id": "TX-000001",
            "transaction_timestamp": "2025-12-19T00:00:00+00:00",
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627", 
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 1000,                                      # and amount NOT above threshold , don't report this one
            "currency": "EUR",
            "is_new_beneficiary": False,
            "beneficiary_account": "PL358075381662562554536117",   # and now we send PL
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        },
        {
            "transaction_id": "TX-000002",
            "transaction_timestamp": "2025-12-19T00:01:00+00:00", # +1 hr
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627", 
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 1000,                                  # and amount NOT above threshold , don't report this one
            "currency": "EUR",
            "is_new_beneficiary": False,
            "beneficiary_account": "DE358075381662562554536117",   # and now we send DE
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        },
        {
            "transaction_id": "TX-000003",
            "transaction_timestamp": "2025-12-19T00:02:00+00:00",  # +2 hr
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627",
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 15001,                                  # and amount above threshold ! report this one
            "currency": "EUR",
            "is_new_beneficiary": False,
            "beneficiary_account": "SE358075381662562554536117",   # and now we send SE
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        }
    ]

    df_input = pd.DataFrame(data)
    df_input["transaction_timestamp"] = pd.to_datetime(df_input["transaction_timestamp"])

    df_output = rule.evaluate(df_input)
    # ensure we have correctly identified transaction TX-000003 with amount over threshold and new country code
    assert len(df_output) == 1
    assert df_output.iloc[0]['transaction_id'] == 'TX-000003'


def test_r10_evaluate_amount_is_under_15k_EUR_DONT_flag_as_fraud___no_country_switch():
    rule = Rule10()

    data = [
        {
            "transaction_id": "TX-000001",
            "transaction_timestamp": "2025-12-19T00:00:00+00:00",
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627",    
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 15000,                                     # equal to threshold
            "currency": "EUR",
            "is_new_beneficiary": False,
            "beneficiary_account": "DE358075381662562554536117",    # we send to DE
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        },
        {
            "transaction_id": "TX-000002",
            "transaction_timestamp": "2025-12-19T00:01:00+00:00",
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627",      
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 14999,                                     # less than threshold, don't report
            "currency": "EUR",
            "is_new_beneficiary": False,
            "beneficiary_account": "PL358075381662562554536117",   # we send to PL
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
    
def test_r10_evaluate_amount_is_under_15k_EUR_DONT_flag_as_fraud___with_country_switch():
    rule = Rule10()

    data = [
        {
            "transaction_id": "TX-000001",
            "transaction_timestamp": "2025-12-19T00:00:00+00:00",
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627",    
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 15000,                                     # equal to threshold
            "currency": "EUR",
            "is_new_beneficiary": False,
            "beneficiary_account": "PL358075381662562554536117",    # we send to  PL
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        },
        {
            "transaction_id": "TX-000002",
            "transaction_timestamp": "2025-12-19T00:01:00+00:00",  # +1 hr
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627",      
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 14999,                                     # less than threshold, don't report
            "currency": "EUR",
            "is_new_beneficiary": False,
            "beneficiary_account": "DE358075381662562554536117",    # we send to  DE
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        },
        {
            "transaction_id": "TX-000003",
            "transaction_timestamp": "2025-12-19T00:01:00+00:00",  # +2 hr
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627",      
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": 14999,                                     # less than threshold, don't report
            "currency": "EUR",
            "is_new_beneficiary": False,
            "beneficiary_account": "NO358075381662562554536117",   # we send to NO
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
    
