from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest

from rules.r17 import Rule17

# if 'pytest' not work for you try following:
# first you need to install few things:
#     pip install pytest
#     pip install .
# then in bash type 'pytest' to exec unit tests
#     pytest


# Trigger if ≥ 5 tx between €13,500–€14,999 in 2h
@pytest.mark.parametrize("tx_number,amount,time_shift_minutes,tx_amount_expected,tx_expected_names", [
    (5, 14000, 10, 1, ["TX-5"]), # 5 transactions every 10 minutes, with all amounts in range, mark last as fraud
    (5, 14000, 30, 0, None), # 5 transactions every 30 minutes, with all amounts in range, no fraud as to much spread over time
    (5, 13499, 10, 0, None), # 5 transactions every 10 minutes, with amounts to low - no fraud
    (5, 15000, 10, 0, None), # 5 transactions every 10 minutes, with amounts too high - no fraud
    (4, 14000, 10, 0, None), # 4 transactions every 10 minutes, with all amounts in range, no fraud as too few tx
    (6, 14000, 10, 2, ["TX-5","TX-6"]), # 6 transactions every 10 minutes, with all amounts in range, 2 tx reported as fraud
])
def test_r17_evaluate_X_tranasctions_in_amount_range_and_time_are_FLAG_as_fraud(tx_number:int, amount:float, time_shift_minutes: int, tx_amount_expected: int, tx_expected_names: list[str]):
    rule = Rule17()

    dt = datetime(2025, 12, 19, 0, 0, 0, tzinfo=timezone.utc)
    
    data = []
    for i in range(tx_number):
        data.append(
        {
            "transaction_id": f'TX-{i+1}',
            "transaction_timestamp": dt.isoformat(),
            "customer_id": 2045,
            "customer_account": "PL270398487102963371148627", 
            "channel": "Mobile",
            "device_id": "MOB-IOS-21E3BCAD",
            "amount": amount,                                   # inject amount
            "currency": "EUR",
            "is_new_beneficiary": False,
            "beneficiary_account": "PL358075381662562554536117",   # we send PL
            "entered_beneficiary_name": "Justyna Brzykcy",
            "official_beneficiary_account_name": "Justyna Brzykcy",
            "customer_account_balance": 455420
        })
        dt = dt + timedelta(minutes=time_shift_minutes)         # control time shift between samples

    df_input = pd.DataFrame(data)
    df_input["transaction_timestamp"] = pd.to_datetime(df_input["transaction_timestamp"])

    df_output = rule.evaluate(df_input)

    assert len(df_output) == tx_amount_expected
    if tx_amount_expected > 0:
        assert df_output["transaction_id"].tolist() == tx_expected_names

