import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from release_one.validation import format_sales
from release_one.decomp import decompose_sales

# select store and tank
store = 144
tank = 2

# load sales data
dat = pd.read_csv(f'./data/sales/KT{store}{tank}_sales.csv',
                  usecols=range(1, 6))
tank_type = dat.tank_type.iloc[-1]

# validate sales data
dat = dat.to_dict(orient="records")
sales_dat = format_sales(dat)

# decompose sales data into GAM curves
decomp = decompose_sales(sales_dat)

# visualize yearly / weekly seasonality
plt.close()
sns.set()
fig, axs = plt.subplots(2)
fig = sns.lineplot(y=decomp[0], x=range(len(decomp[0])), ax=axs[0]).set_title(f'KT{store}: Fuel type {tank_type}')
fig = sns.lineplot(y=decomp[1], x=range(len(decomp[1])), ax=axs[1])
plt.savefig(fname=f'./figures/decompose/sales/KT{store}{tank}_season_decomp.png')
plt.show()




