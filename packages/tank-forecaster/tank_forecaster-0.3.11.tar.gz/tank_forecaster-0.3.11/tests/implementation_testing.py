import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from release_one.validation import format_sales, format_tank, validate_tank
from release_one.decomp import decompose_sales
from release_one.forecaster import forecast_near, forecast_far
from release_one.events import standard_events, add_events, apply_event_factor

#### tanks with entire dataset #################

# forecast far w/ custom events >52 weeks

store = 144
tank = 2
dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/sales/KT{store}{tank}_sales.csv',
                  usecols=range(1, 6))
tank_type = dat.tank_type.iloc[-1]
sales_dat = dat.to_dict(orient='records')

# create forecast
sales_dat = format_sales(sales_dat)
decomp = decompose_sales(sales_dat)
forecast = forecast_far(sales_dat,
                        forecast_length=300,
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

# visualize
fig = sns.lineplot(x=new_forecast.ds, y=new_forecast.yhat, color='black', alpha=0.7)
fig.legend(['no event adjustments', 'event adjustments'])
fig.set(ylabel='daily sales in gallons', xlabel='date')
plt.show()

# forecast near w/ events >52 weeks data

# data in db format
store = 144
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
                        dates=['2020-06-05'],
                        factors=[1.5])

new_forecast = apply_event_factor(forecast, new_events, output='df')

fig2 = sns.lineplot(x=new_forecast.ds, y=new_forecast.yhat, color='black', alpha=0.7)
fig2.legend(['no event adjustments', 'event adjustments'])
fig2.set(ylabel='daily sales in gallons', xlabel='date')
plt.savefig(fname=f'./figures/forecast_near/event_adjustment.png')
plt.show()





#### tanks with reduced dataset #################

# forecast far w/ standard events <52 weeks

# load and format sales data
store = 144
tank = 2

# data in db format
dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/sales/KT{store}{tank}_sales.csv',
                  usecols=range(1, 6))
tank_type = dat.tank_type.iloc[-1]

train = dat.iloc[1029:1128]  # 100 days
test = dat.iloc[1128:]

train = train.to_dict(orient='records')
test = test.to_dict(orient='records')

# format
train = format_sales(train)
test = format_sales(test)

# create forecast, apply events
decomp = decompose_sales(train)
forecast = forecast_far(train,
                        forecast_length=200,
                        yearly_decomp=decomp[0],
                        weekly_decomp=decomp[1])

forecast = apply_event_factor(forecast=forecast,
                              events=standard_events,
                              output='ds')


# visualize results
plt.close()
sns.set()
fig = sns.lineplot(x=forecast.ds, y=forecast.yhat, color='blue', alpha=0.7)
fig = sns.lineplot(x=test.ds, y=test.y, color='black', alpha=0.7)
fig.legend(['forecast', 'actual'])
fig.set(ylabel='daily sales in gallons', xlabel='date')
plt.show()


# forecast near with standard events <52 weeks
store = 144
tank = 1

dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/tank/kt{store}_tank_history.csv')
dat = dat.loc[(dat.tank_id == tank)]
dat = dat.to_dict(orient="records")
tank_dat = format_tank(dat)

train = tank_dat.iloc[6200:6500]
test = tank_dat.iloc[6500:]

test
# load and format sales data for validation
store = 144
tank = 2
dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/sales/KT{store}{tank}_sales.csv',
                  usecols=range(1, 6))
dat = dat.to_dict(orient="records")
sales = format_sales(dat)


# validate tank data & forecast
train = validate_tank(train, sales)
forecast = forecast_near(train, forecast_length=144)
forecast = apply_event_factor(forecast, standard_events)#s, output='df')

plt.close()
sns.set()
fig2 = sns.lineplot(x=forecast.ds, y=forecast.yhat, color='blue', alpha=0.7)
fig2 = sns.lineplot(x=test.ds[:144], y=test.y[:144], color='black', alpha=0.7)
fig2.legend(['prediction', 'actual'])
fig2.set(ylabel='daily sales in gallons', xlabel='date')
plt.show()




##### New Tank, No Data ###############

# forecast far - no data
sales = []

decomp = decompose_sales(sales)  # returns generic

forecast = forecast_far(sales,
                        forecast_length=200,
                        yearly_decomp=decomp[0],
                        weekly_decomp=decomp[1],
                        daily_lift_est=1000) # daily est lift required

forecast = apply_event_factor(forecast=forecast,
                              events=standard_events,
                              output='df') # standard events


# visualize results
plt.close()
sns.set()
fig = sns.lineplot(x=forecast.ds, y=forecast.yhat, color='blue', alpha=0.7)
fig.legend(['forecast', 'actual'])
fig.set(ylabel='daily sales in gallons', xlabel='date')
plt.show()

# forecast near -  no data
tank = []
sales = []

# validate tank data & forecast
train = validate_tank(tank, sales)
train

forecast = forecast_near(train, forecast_length=144)
forecast

forecast = apply_event_factor(forecast, standard_events, output='df')
forecast

plt.close()
sns.set()
fig2 = sns.lineplot(x=forecast.ds, y=forecast.yhat, color='blue', alpha=0.7)
fig2 = sns.lineplot(x=test.ds[:144], y=test.y[:144], color='black', alpha=0.7)
fig2.legend(['prediction', 'actual'])
fig2.set(ylabel='daily sales in gallons', xlabel='date')
plt.show()


