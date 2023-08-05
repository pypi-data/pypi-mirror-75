import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from release_one.validation import format_sales, format_tank, validate_tank
from release_one.forecaster import forecast_near, gen_future


# load and format sales data
store = 144
tank = 2

dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/sales/KT{store}{tank}_sales.csv',
                  usecols=range(1, 6))
tank_type = dat.tank_type.iloc[-1]
sales_dat = dat.to_dict(orient='records')
sales_dat = format_sales(sales_dat)
sales_dat

# load and format tank data
store = 144
tank = 1

dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/tank/old/kt{store}_tank_history.csv')
dat = dat.loc[(dat.tank_id == tank)]
dat = dat.to_dict(orient="records")
tank_dat = format_tank(dat)


# validate tank data
tank_dat = validate_tank(tank_dat, sales_dat)
tank_dat


# test train split
train = tank_dat[:int(0.74*len(tank_dat))]
test = tank_dat[int(0.74*len(tank_dat)):]

# short term forecast
forecast = forecast_near(train, forecast_length=144)


# visualize results
plt.close()
sns.set()
fig = sns.lineplot(x=test.ds[:144], y=test.y[:144], color='black', alpha=0.7)
fig = sns.lineplot(x=forecast.ds, y=forecast.yhat, color='blue', alpha=0.7)
fig.set_title('')
fig.legend(['Actual Sales', 'Forecasted Sales'])
fig.set(ylabel='Half-Hour Sales in Gallons', xlabel='Date')
# plt.savefig(fname=f'./figures/forecast_near/KT{store}{tank}_2.png')
plt.show()


