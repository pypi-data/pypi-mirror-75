#!/usr/bin/env python

import numpy as np
import pandas as pd

from tank_forecaster import validation


def test_working():
    x = True
    assert x


def test_format_tank_none():
    x = validation.format_tank(None)
    assert x is None


def test_format_tank_empty():
    x = validation.format_tank([])
    assert x is None


def test_format_tank_two_entries(tank_two_entry_input):
    x = validation.format_tank(tank_two_entry_input)
    assert x is None


def test_format_tank_proper(tank_little_input):
    x = validation.format_tank(tank_little_input)
    assert type(x) is pd.core.frame.DataFrame
    assert len(x['ds']) != 0
    assert len(x['y']) != 0
    assert type(x.ds.iloc[-1]) is pd._libs.tslibs.timestamps.Timestamp
    assert type(x.y.iloc[-1]) is np.float64


def test_format_sales_none():
    x = validation.format_sales(None)
    assert x is None


def test_format_sales_empty():
    x = validation.format_sales([])
    assert x is None


def test_format_sales_proper(sales_little_input):
    x = validation.format_sales(sales_little_input)
    assert type(x) is pd.core.frame.DataFrame
    assert len(x['ds']) != 0
    assert len(x['y']) != 0
    assert type(x.ds.iloc[-1]) is pd._libs.tslibs.timestamps.Timestamp
    assert type(x.y.iloc[-1]) is np.float64
    # change
