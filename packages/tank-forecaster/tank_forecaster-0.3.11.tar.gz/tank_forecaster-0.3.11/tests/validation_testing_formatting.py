# libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from release_one.validation import format_tank, format_sales

# tank sticking for test formatting
dat = pd.read_csv('./data/tank/kt141_tank_history.csv')
dat = dat.loc[(dat.tank_id == 1)]
dat = dat.drop(dat.columns[4], axis=1)

# original data
plt.close()
sns.set()
sns.lineplot(y=dat.volume[:50], x=dat.read_time[:50])
plt.show()

# format tank sticking
tank_dat = dat.to_dict(orient="records")
tank_dat = format_tank(tank_dat)

# formatted data
plt.close()
sns.lineplot(y=tank_dat.y, x=tank_dat.ds)
plt.show()




# sales data for test formatting
dat = pd.read_csv('./data/sales/KT3116_sales.csv',
                  usecols=[1, 2, 3, 4, 5])

# original data
plt.close()
plt.plot(dat.sales)
plt.show()

# format data
sales_dat = dat.to_dict(orient="records")
sales_dat = format_sales(sales_dat)

# formatted data
plt.close()
plt.plot(sales_dat.y)
plt.show()
