import numpy as np
import pandas as pd

from release_one.events import standard_events, remove_event_factor

generic_sales = pd.DataFrame({'ds': pd.date_range(start='2020-01-01',
                                                  end='2020-12-31', freq='1D'),
                              'y': np.repeat(100, 366)})

generic_tank = pd.DataFrame({'ds': pd.date_range(start='2020-12-24',
                                               end='2021-01-02', freq='30min'),
                           'y': np.repeat(100, 433)})

# sales history

sns.set()
sns.lineplot(x=generic_sales.ds, y=generic_sales.y)
plt.show()

test = remove_event_factor(generic_sales, standard_events)
test

sns.set()
sns.lineplot(x=test.ds, y=test.y)
plt.show()


# tank history

sns.set()
sns.lineplot(x=generic_tank.ds, y=generic_tank.y)
plt.show()

test2 = remove_event_factor(generic_tank, standard_events)
test2

sns.set()
sns.lineplot(x=test2.ds, y=test2.y)
plt.show()