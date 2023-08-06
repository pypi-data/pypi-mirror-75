#!/usr/bin/env python

from tank_forecaster import decomp

def test_decomp_sales_none():
    x = decomp.decompose_sales(None)
    assert len(x[0]) == 53 # generic yearly
    assert len(x[1]) == 7  # generic weekly

def test_decomp_sales_proper(sales_proper):
    x = decomp.decompose_sales(sales_proper)
    assert len(x[0]) != 0
    assert len(x[1]) != 0


