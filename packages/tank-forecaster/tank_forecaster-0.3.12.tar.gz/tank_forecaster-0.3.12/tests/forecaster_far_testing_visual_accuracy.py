import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from release_one.validation import format_sales
from release_one.decomp import decompose_sales
from release_one.forecaster import forecast_far


# declare store / tank
store = 381
tank = 2


# load sales data & save fuel type
dat = pd.read_csv(f'./data/sales/KT{store}{tank}_sales.csv',
                  usecols=range(1, 6))
tank_type = dat.tank_type.iloc[-1]


# format and split dataset
dat = dat.to_dict(orient="records")
dat = format_sales(dat)
train = dat.iloc[:int(0.85*len(dat))]
test = dat.iloc[int(0.85*len(dat)):]


# decompose sales data into GAM curves
decomp = decompose_sales(train)


# long term forecast
forecast = forecast_far(train,
                        forecast_length=360,
                        yearly_decomp=decomp[0],
                        weekly_decomp=decomp[1])

# show and save figure
plt.close()
sns.set()
fig = sns.lineplot(x=test.ds[:360], y=test.y[:360], color='black', alpha=0.5)
fig = sns.lineplot(x=forecast.ds, y=forecast.yhat, color='blue', alpha=0.7)
fig.set_title(f'KT{store}: Fuel type {tank_type}')
fig.legend(['Actual Sales', 'Forecasted Sales'])
fig.set(ylabel='Daily Sales in Gallons', xlabel='Date')
fig.set_title('')
# plt.savefig(fname=f'./figures/forecast_far/KT{store}{tank}.png')
plt.show()


