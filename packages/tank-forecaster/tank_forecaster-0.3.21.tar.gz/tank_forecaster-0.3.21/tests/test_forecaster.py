import pandas as pd
import numpy as np

from tank_forecaster import forecaster


def test_far_none():
    x = forecaster.forecast_far(None, daily_lift_est=1000)
    assert type(x) is pd.core.frame.DataFrame
    assert 'ds' in x and 'yhat' in x
    assert len(x) == 90
    assert type(x.ds.iloc[-1]) is pd._libs.tslibs.timestamps.Timestamp
    assert type(x.yhat.iloc[-1]) is np.float64


def test_far_little_data(sales_little_data):
    x = forecaster.forecast_far(sales_little_data)
    assert type(x) is pd.core.frame.DataFrame
    assert 'ds' in x and 'yhat' in x
    assert len(x) == 90
    assert type(x.ds.iloc[-1]) is pd._libs.tslibs.timestamps.Timestamp
    assert type(x.yhat.iloc[-1]) is np.float64


def test_far_proper():
    pass


def test_near_none():
    x = forecaster.forecast_near(None, daily_lift_est=1000)
    assert type(x) is pd.core.frame.DataFrame
    assert len(x) == 144
    assert 'ds' in x and 'yhat' in x
    assert type(x.ds.iloc[-1]) is pd._libs.tslibs.timestamps.Timestamp
    assert type(x.yhat.iloc[-1]) is np.float64


def test_near_little_data(tank_little_data):
    x = forecaster.forecast_near(tank_little_data)
    assert type(x) is pd.core.frame.DataFrame
    assert len(x) == 144
    assert 'ds' in x and 'yhat' in x
    assert type(x.ds.iloc[-1]) is pd._libs.tslibs.timestamps.Timestamp
    assert type(x.yhat.iloc[-1]) is np.float64


def test_near_proper():
    pass
