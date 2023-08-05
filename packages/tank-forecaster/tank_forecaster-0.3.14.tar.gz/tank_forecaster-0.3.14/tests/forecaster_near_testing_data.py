import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from validation import validate_sales, validate_tank
from ne.decomp import decompose_sales, decompose_tank, generic_daily_decomp, generic_yearly_decomp, generic_weekly_decomp
from release_one.forecaster import forecast_far, forecast_near


# run long term forecast first
store = 166
tank = 2

# load
dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/sales/KT{store}{tank}_sales.csv',
                  usecols=range(1, 6))
dat.date = pd.to_datetime(dat.date, format='%Y-%m-%d')

# validate
sales_dat = dat.to_dict(orient='records')
sales_dat = validate_sales(sales_dat)

# decompose
sales_decomp = decompose_sales(sales_dat)

# forecast
sales_forecast = forecast_far(sales_dat,
                             yearly_decomp=sales_decomp[0],
                             weekly_decomp=sales_decomp[1],
                             forecast_length=90,
                             output_format='df')
sales_forecast


# short term forecast

store = 166
tank = 1

dat = pd.read_csv(f'/Users/fisherankney/workspace/forecaster_local/data/demo/raw/kt{store}_tank_history.csv')
dat = dat[dat['tank_id'] == 1]
dat = dat.to_dict(orient="records")
dat = validate_tank(dat)

# not enough data
no_data = dat[-2:]
no_data
len(no_data) # under 'no data' threshold (432)

if __name__ == '__main__':
    stf = forecast_near(tank_history=no_data, sales_history=sales_dat,
                        forecast_length=144, output_format='df')

plt.close()
sns.set()
fig = sns.lineplot(x=range(0,432), y=predictions, color='blue', alpha=0.7)
plt.show()




# sufficient data
tank_data = dat
len(tank_data) # above 'no data' threshold

forecast_near(tank_history=tank_data, sales_history=sales_dat,
              forecast_length=144, output_format='df') # should run w/out need of sales dat
