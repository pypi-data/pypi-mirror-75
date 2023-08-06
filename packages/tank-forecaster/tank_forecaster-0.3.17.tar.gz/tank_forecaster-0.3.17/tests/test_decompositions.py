from tank_forecaster import decomp


def test_decomp_sales_none():
    x = decomp.decompose_sales(None)
    assert len(x[0]) == 53  # generic yearly
    assert len(x[1]) == 7  # generic weekly


def test_decomp_sales_little_data(sales_little_data):
    x = decomp.decompose_sales(sales_little_data)
    assert len(x[0]) != 0
    assert len(x[1]) != 0


def test_decomp_sales_proper_data():
    pass
