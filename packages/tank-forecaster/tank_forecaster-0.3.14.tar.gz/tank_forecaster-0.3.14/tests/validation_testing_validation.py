import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from release_one.validation import *

# tank sticking data, formatted
dat = pd.read_csv('./data/demo/raw/kt141_tank_history.csv')
dat = dat.loc[(dat.tank_id == 1)]
dat = dat.drop(dat.columns[4], axis=1)
dat = dat.to_dict(orient="records")
tank_dat = format_tank(dat)

# sales data, formatted
dat = pd.read_csv('./data/sales/KT1442_sales.csv',
                  usecols=[1, 2, 3, 4, 5])
sales_dat = dat.to_dict(orient="records")
sales_dat = format_sales(sales_dat)



# adjusting tank data histories - test cases
# normal tank data
full_tank = tank_dat.iloc[-432:]
full_tank.reset_index(inplace=True, drop=True)

out = validate_tank(tank_data=full_tank, sales_data=sales_dat)
plt.close()

sns.set()
fig = sns.lineplot(x=out.index, y=out.actual, color = 'blue', alpha=0.7)
fig = sns.lineplot(x=out.index, y=out.estimated, color = 'red', alpha=0.7)
fig.set_title('data validation example 1 (normal tank)')
fig.legend(['actuals', 'estimated'])
# plt.savefig(fname=f'./figures/data_validation_ex1.png')
plt.show()


# older tank data
old_tank = tank_dat.iloc[-432-200:-200]
old_tank.reset_index(inplace=True, drop=True)

out = validate_tank(tank_data=old_tank, sales_data=sales_dat)
out

plt.close()
sns.set()
fig = sns.lineplot(x=out.index, y=out.actual, color='blue', alpha=0.7)
fig = sns.lineplot(x=out.index, y=out.estimated, color='red', alpha=0.7)
fig.set_title('data validation example 2 (older tank)')
fig.legend(['unadjusted', 'adjusted'])
# plt.savefig(fname=f'./figures/data_validation_ex2.png')
plt.show()




# half a tank worth of data
half_tank = tank_dat.iloc[-250:]
half_tank.reset_index(inplace=True, drop=True)

out = validate_tank(tank_data=half_tank, sales_data=sales_dat)
out

plt.close()
sns.set()
fig = sns.lineplot(x=out.index, y=out.actual, color = 'blue', alpha=0.7)
fig = sns.lineplot(x=out.index, y=out.estimated, color = 'red', alpha=0.7)
fig = sns.lineplot(x=out.index, y=out.output, color='green', alpha=0.7)
fig.set_title('data validation example 3 (half tank)')
fig.legend(['unadjusted', 'adjusted', 'output'])
plt.savefig(fname=f'./figures/data_validation_ex3.png')
plt.show()


# missing data
missing_tank = pd.concat([tank_dat.iloc[-300:-200], tank_dat.iloc[-50:]], ignore_index=True)
missing_tank.reset_index(inplace=True, drop=True)

out = validate_tank(tank_data=missing_tank, sales_data=sales_dat)
out

plt.close()
sns.set()
fig = sns.lineplot(x=out.index, y=out.actual, color = 'blue', alpha=0.7)
fig = sns.lineplot(x=out.index, y=out.estimated, color = 'red', alpha=0.7)
fig = sns.lineplot(x=out.index, y=out.output, color='green', alpha=0.7)
fig.set_title('data validation example 4')
fig.legend(['unadjusted', 'adjusted', 'output'])
# plt.savefig(fname=f'./figures/data_validation_ex4.png')
plt.show()


no_tank = tank_dat.iloc[0:0]

out = validate_tank(tank_data=no_tank, sales_data=sales_dat)
out
forecast_near(out,



plt.close()
sns.set()
fig = sns.lineplot(x=out.index, y=out.actual, color = 'blue', alpha=0.7)
fig = sns.lineplot(x=out.index, y=out.estimated, color = 'red', alpha=0.7)
fig = sns.lineplot(x=out.index, y=out.output, color='green', alpha=0.7)
fig.set_title('data validation example 5 (no data) - obv not working')
fig.legend(['unadjusted', 'adjusted', 'output'])
# plt.savefig(fname=f'./figures/data_validation_ex5.png')
plt.show()