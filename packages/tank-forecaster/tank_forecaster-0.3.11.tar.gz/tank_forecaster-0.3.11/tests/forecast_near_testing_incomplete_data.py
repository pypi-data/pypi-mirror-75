import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from release_one.validation import format_sales, format_tank, validate_tank
from release_one.forecaster import forecast_near


# load and format sales data
store = 144
tank = 2

dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/sales/KT{store}{tank}_sales.csv',
                  usecols=range(1, 6))
tank_type = dat.tank_type.iloc[-1]
sales_dat = dat.to_dict(orient='records')
sales_dat = format_sales(sales_dat)


# load and format tank data
store = 144
tank = 1

dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/tank/kt{store}_tank_history.csv')
dat = dat.loc[(dat.tank_id == tank)]
dat = dat.to_dict(orient="records")
tank_dat = format_tank(dat)


# test train split
train_full = tank_dat[:int(0.75*len(tank_dat))]
test = tank_dat[int(0.75*len(tank_dat)):]

# incomplete training data
train = train_full.iloc[-100:]
train

# if __name__ == '__main__':
train_val = validate_tank(tank_data=train, sales_data=sales_dat)
train_val

plt.close()
sns.set(rc={'figure.figsize':(11.7,8.27)})
fig = sns.lineplot(x=train_val.ds, y=train_val.actual, color='blue', alpha=0.9)
fig = sns.lineplot(x=train_val.ds, y=train_val.estimated, color='orange', alpha=0.9)
fig = sns.lineplot(x=train_val.ds, y=train_val.output, color='green', alpha=0.9)
fig = sns.lineplot(x=train_full.ds[-432:], y=train_full.y[-432:], color='black', alpha=0.4)
fig.legend(['actual (present)', 'estimated', 'used in model', 'actual (artificially missing)'])
plt.savefig(fname=f'./figures/forecast_near/missing_data_testing_10.png')
plt.show()

# short term forecast without validation
# forecast = forecast_near(train, forecast_length=144, output_format='df')
# forecast_v = forecast_near(train_val, forecast_length=144, output_format='df')


# visualize results
# plt.close()
# fig = sns.lineplot(x=forecast.ds, y=forecast.yhat, color='blue', alpha=0.7)
# fig = sns.lineplot(x=forecast_v.ds, y=forecast_v.yhat, color='green', alpha=0.7)
# fig = sns.lineplot(x=test.ds[:144], y=test.y[:144], color='black', alpha=0.7)
# fig.set_title(f'KT{store}: Fuel type {tank_type}')
# fig.legend(['no validation', 'validation', 'actual sales'])
# fig.set(ylabel='half-hour sales in gallons', xlabel='date')
# plt.savefig(fname=f'./figures/forecast_near/missing_data_testing_7.png')
# plt.show()

