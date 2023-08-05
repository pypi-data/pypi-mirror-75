import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from release_one.validation import format_sales, format_tank
from release_one.decomp import decompose_sales, decompose_tank
from release_one.forecaster import forecast_far, forecast_near

# conduct long term forecast
store = 390
tank = 2

dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/sales/KT{store}{tank}_sales.csv',
                  usecols=range(1, 6))
dat.date = pd.to_datetime(dat.date, format='%Y-%m-%d')
train_sales = dat.iloc[:3795]
test_sales = dat.iloc[3975:]
train_sales = train_sales.to_dict(orient="records")
train_sales = format_sales(train_sales)
decomp = decompose_sales(train_sales)

ltf = forecast_far(train_sales, yearly_decomp=decomp[0], weekly_decomp=decomp[1],
                 forecast_length=90, holiday_decomp=[], custom_events=[],
                 event_factors=[], daily_lift_est=0, output_format='df')


# conduct short term forecast
store = 390
tank = 1

dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/demo/raw/kt{store}_tank_history.csv')
dat = dat[dat['tank_id'] == 1]
dat = dat.to_dict(orient="records")

# validate data
dat = format_tank(dat)
train_tank = dat[:-144]
test_tank = dat[-144:]
test_tank
stf = forecast_near(train_tank, forecast_length=144, output_format='df')

plt.close()
sns.set()
fig = sns.lineplot(x=ltf.ds, y=ltf.yhat, color='blue', alpha=0.7)
plt.show()

plt.close()
sns.set()
fig = sns.lineplot(x=stf.ds, y=stf.yhat, color='blue', alpha=0.7)
plt.show()

from release_one.decomp import generic_daily_decomp
from release_one.decomp import decompose_tank

tank_decomp = decompose_tank(train_tank)
tank_decomp.daily
predictions = pd.DataFrame(columns=['day', 'day_sum',
                                    'hour', 'hour_base',
                                    'hour_estimate'])
predictions['day'] = np.repeat(ltf.ds[:3], 48)
predictions['day_sum'] = np.repeat(ltf.yhat[:3], 48)
predictions['hour'] = np.repeat(tank_decomp.index, 3)
predictions['hour_base'] = predictions.day_sum*(1/48)
daily_rep = pd.concat([tank_decomp.daily] * 3, ignore_index=True)
predictions.reset_index(inplace=True, drop=True)
predictions['hour_estimate'] = predictions.hour_base * daily_rep
predictions

# compare to
plt.close()
sns.set()
fig = sns.lineplot(x=predictions.index, y=predictions.hour_estimate, color='blue', alpha=0.7)
fig = sns.lineplot(x=range(0,144), y=stf.yhat, color='red', alpha=0.7)
plt.show()

# compare to generic decomposition

from release_one.decomp import generic_daily_decomp

preds = pd.DataFrame(columns=['day', 'day_sum',
                                    'hour', 'hour_base',
                                    'hour_estimate'])
preds['day'] = np.repeat(ltf.ds[:3], 48)
preds['day_sum'] = np.repeat(ltf.yhat[:3], 48)
preds['hour'] = np.repeat(tank_decomp.index, 3)
preds['hour_base'] = predictions.day_sum*(1/48)
daily_rep = pd.concat([generic_daily_decomp] * 3, ignore_index=True)
preds.reset_index(inplace=True, drop=True)
preds['hour_estimate'] = preds.hour_base * daily_rep
preds


# compare to
plt.close()

sns.set(rc={'figure.figsize':(8,6)})
fig = sns.lineplot(x=range(0,144), y=test_tank.y, color='black', alpha = 0.7)
fig = sns.lineplot(x=predictions.index, y=predictions.hour_estimate, color='blue', alpha=0.7)
fig = sns.lineplot(x=preds.index, y=preds.hour_estimate, color='green', alpha=0.7)
fig = sns.lineplot(x=range(0,144), y=stf.yhat, color='red', alpha=0.7)
fig.legend(['actual', '1', '2', '3'])
fig.set(ylabel='change in tank level', xlabel='# half hours from prediction')

plt.savefig(fname=f'../figures/forecast_near_validation/KT{store}{tank}.png')
plt.show()
