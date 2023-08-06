import pytest
import pandas as pd


@pytest.fixture(scope='module')
def tank_two_entry_input():
    return [{'product': 'UNLEADED 88',
               'read_time': '2020-07-22T12:35:01',
               'run_time': '2020-07-22T12:35:01',
               'store_number': 'KT110',
               'tank_id': '1',
               'temperature': 66.5836944411236,
               'volume': 13284.172673874453},
              {'product': 'UNLEADED 88',
               'read_time': '2020-07-22T12:24:01',
               'run_time': '2020-07-22T12:24:00',
               'store_number': 'KT110',
               'tank_id': '1',
               'temperature': 66.5805883403786,
               'volume': 13298.881427020242}]


@pytest.fixture(scope='module')
def tank_little_input():
    return [{'product': 'UNLEADED 88',
               'read_time': '2020-07-22T12:35:01',
               'run_time': '2020-07-22T12:35:01',
               'store_number': 'KT110',
               'tank_id': '1',
               'temperature': 66.5836944411236,
               'volume': 13284.172673874453},
              {'product': 'UNLEADED 88',
               'read_time': '2020-07-22T12:24:01',
               'run_time': '2020-07-22T12:24:00',
               'store_number': 'KT110',
               'tank_id': '1',
               'temperature': 66.5805883403786,
               'volume': 13298.881427020242},
            {'product': 'UNLEADED 88',
             'read_time': '2020-07-22T12:15:01',
             'run_time': '2020-07-22T12:15:00',
             'store_number': 'KT110',
             'tank_id': '1',
             'temperature': 66.5805883403786,
             'volume': 1410.881427020242},
            {'product': 'UNLEADED 88',
             'read_time': '2020-07-22T11:55:01',
             'run_time': '2020-07-22T11:55:00',
             'store_number': 'KT110',
             'tank_id': '1',
             'temperature': 66.5805883403786,
             'volume': 1450.881427020242},
            {'product': 'UNLEADED 88',
             'read_time': '2020-07-22T11:25:01',
             'run_time': '2020-07-22T11:25:00',
             'store_number': 'KT110',
             'tank_id': '1',
             'temperature': 66.5805883403786,
             'volume': 1470.881427020242}
            ]


@pytest.fixture(scope='module')
def tank_little_data():
    df = pd.DataFrame(
        data=[
            ['2020-07-04 13:30:00', 25],
            ['2020-07-04 14:00:00', 50],
            ['2020-07-04 14:30:00', 75],
            ['2020-07-04 15:00:00', 50],
            ['2020-07-04 15:30:00', 50]

        ],
        columns=['ds', 'y']
    )

    df.ds = pd.to_datetime(df.ds)

    return df


@pytest.fixture(scope='module')
def sales_little_input():
    return [{'store': '103', 'date': '2017-06-05', 'tank_id': '1', 'tank_type': '304', 'sales': 23},
            {'store': '103', 'date': '2017-06-04', 'tank_id': '1', 'tank_type': '304', 'sales': 51},
            {'store': '103', 'date': '2017-06-03', 'tank_id': '1', 'tank_type': '304', 'sales': 43},
            {'store': '103', 'date': '2017-06-02', 'tank_id': '1', 'tank_type': '304', 'sales': 10}]


@pytest.fixture(scope='module')
def sales_little_data():
    df = pd.DataFrame(
        data=[
            ['2020-07-04', 25],
            ['2020-07-03', 50],
            ['2020-07-02', 75],
            ['2020-07-01', 50]
        ],
        columns=['ds', 'y']
    )

    df.ds = pd.to_datetime(df.ds)

    return df
