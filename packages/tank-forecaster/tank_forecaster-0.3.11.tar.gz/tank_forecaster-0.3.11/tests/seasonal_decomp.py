import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fbprophet import Prophet

from release_one.validation import format_tank, format_sales

dat = pd.read_csv(f'data/tank/kt144_tank_history.csv', usecols=range(1, 6))
dat = dat.loc[dat['tank_id'] == 1]
dat = dat.to_dict(orient="records")
tank_dat = format_tank(dat)
tank_dat

m = Prophet(changepoint_prior_scale=0.05,
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=True,
            seasonality_mode='multiplicative')
mod = m.fit(tank_dat)
future = m.make_future_dataframe(periods=150, freq='1D')
forecast = m.predict(future)

m.plot_components(forecast)
plt.show()



dat = pd.read_csv('/Users/fisherankney/workspace/forecaster_local/data/sales/KT1042_sales.csv')
dat = dat.to_dict(orient="records")
sales_dat = format_sales(dat)

m = Prophet(changepoint_prior_scale=0.05,
            daily_seasonality=False,
            weekly_seasonality=False,
            yearly_seasonality=True,
            seasonality_mode='multiplicative')
mod = m.fit(sales_dat)
future = m.make_future_dataframe(periods=150, freq='1D')
forecast = m.predict(future)

m.plot_components(forecast)
plt.show()
