from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest

from rules.r18 import Rule18

# if 'pytest' not work for you try following:
# first you need to install few things:
#     pip install pytest
#     pip install .
# then in bash type 'pytest' to exec unit tests
#     pytest


# Trigger if ≥ 3 round‑number (e)  tx in 48h and amount multiple of 10
@pytest.mark.parametrize("tx_number,amount,time_shift_minutes,tx_amount_expected,tx_expected_names", [
    (3, 10000, 1*60, 1, ["TX-3"]), # 3 transactions every 1 hour, with round amounts in range, mark last as fraud
    (3, 10001, 1*60, 0, None), # 3 transactions every 1 hour, with NOT-round amounts in range, is not fraud
    (2, 10000, 1*60, 0, None), # 2 transactions every 1 hour, with round amounts in range, too few tx - is not fraud
    (4, 10000, 11*60, 2, ["TX-3","TX-4"]), # 4 transactions every 11 hour, with round amounts in range, mark last 2 as fraud
    (3, 10000, 25*60, 0, None), # 3 transactions every 25 hour, with round amounts in range, spread too much over time - no fraud
])
def test_r18_evaluate_X_tranasctions_in_amount_range_and_time_are_FLAG_as_fraud(tx_number:int, amount:float, time_shift_minutes: int, tx_amount_expected: int, tx_expected_names: list[str]):
    rule = Rule18()

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

