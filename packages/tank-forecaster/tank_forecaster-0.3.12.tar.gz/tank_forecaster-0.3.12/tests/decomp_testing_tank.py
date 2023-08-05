import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from release_one.validation import validate_tank
from release_one.decomp import decompose_tank

store = 166
tank = 1

# load tank data
dat = pd.read_csv(f'./data/tank/kt{store}_tank_history.csv')
dat = dat[dat['tank_id'] == tank]

# validate sales data
dat = dat.to_dict(orient="records")
tank_dat = format_tank(dat)

# decompose tank data into GAM curves
decomp = decompose_tank(tank_dat)

# visualize seasonality
plt.close()
sns.set()
fig = sns.lineplot(y=decomp.daily, x=range(0, 48)).set_title(f'KT{store}: tank number {tank}')
plt.savefig(fname=f'./figures/decompose/tank/KT{store}{tank}_daily_decomp.png')
plt.show()

