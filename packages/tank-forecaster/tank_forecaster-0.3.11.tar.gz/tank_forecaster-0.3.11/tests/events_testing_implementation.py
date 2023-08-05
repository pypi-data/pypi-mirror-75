import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from release_one.validation import format_sales, format_tank, validate_tank
from release_one.decomp import decompose_sales
from release_one.forecaster import forecast_near, forecast_far
from release_one.events import standard_events, add_events, apply_event_factor


# forecast far w/ events

# load and format sales data
store = 813
tank = 2

# data in db format
dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/sales/KT{store}{tank}_sales.csv',
                  usecols=range(1, 6))
dat = dat.loc[:3797]
tank_type = dat.tank_type.iloc[-1]
sales_dat = dat.to_dict(orient='records')

# create forecast
sales_dat = format_sales(sales_dat)
decomp = decompose_sales(sales_dat)
forecast = forecast_far(sales_dat,
                        forecast_length=45,
                        yearly_decomp=decomp[0],
                        weekly_decomp=decomp[1])

plt.close()
sns.set()
fig = sns.lineplot(x=forecast.ds, y=forecast.yhat, color='blue', alpha=0.7)

# add new events
new_events = add_events(standard_events,
                        names=['special event 1',
                               'special event 2'],
                        dates=['2020-06-25',
                               '2020-07-05'],
                        factors=[5,
                                 0.2])

# apply events
new_forecast = apply_event_factor(forecast, new_events, output='df')


fig = sns.lineplot(x=new_forecast.ds, y=new_forecast.yhat, color='black', alpha=0.7)
fig.legend(['no event adjustments', 'event adjustments'])
fig.set(ylabel='daily sales in gallons', xlabel='date')
plt.savefig(fname=f'./figures/forecast_far/event_adjustment.png')
plt.show()




# forecast near w/ events

# data in db format
store = 813
tank = 1

dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/tank/kt{store}_tank_history.csv')
dat = dat.loc[(dat.tank_id == tank)]
dat = dat.to_dict(orient="records")
tank_dat = format_tank(dat)


# validate tank data & forecast
tank_dat = validate_tank(tank_dat, sales_dat)
forecast = forecast_near(tank_dat, forecast_length=144)

plt.close()
sns.set()
fig2 = sns.lineplot(x=forecast.ds, y=forecast.yhat, color='blue', alpha=0.7)

# create and apply event
new_events = add_events(standard_events,
                        names=['special event 3'],
                        dates=['2020-05-26'],
                        factors=[1.5])

new_forecast = apply_event_factor(forecast, new_events, output='df')

fig2 = sns.lineplot(x=new_forecast.ds, y=new_forecast.yhat, color='black', alpha=0.7)
fig2.legend(['no event adjustments', 'event adjustments'])
fig2.set(ylabel='daily sales in gallons', xlabel='date')
plt.savefig(fname=f'./figures/forecast_near/event_adjustment.png')
plt.show()