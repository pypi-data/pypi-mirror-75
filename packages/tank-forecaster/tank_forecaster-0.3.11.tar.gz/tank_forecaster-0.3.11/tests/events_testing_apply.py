import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from release_one.events import standard_events, apply_event_factor

generic_daily = pd.DataFrame({'ds': pd.date_range(start='2020-01-01',
                                                  end='2020-12-31', freq='1D'),
                              'yhat': np.repeat(100, 366)})

generic_hh = pd.DataFrame({'ds': pd.date_range(start='2020-12-24',
                                               end='2021-01-02', freq='30min'),
                           'yhat': np.repeat(100, 433)})


# long term forecast

sns.set()
sns.lineplot(x=generic_hh.ds, y=generic_hh.yhat)
plt.show()

test = apply_event_factor(generic_daily, standard_events)
test

sns.set()
sns.lineplot(x=test.ds, y=test.yhat)
plt.show()


# short term forecast

sns.set()
sns.lineplot(x=generic_hh.ds, y=generic_hh.yhat)
plt.show()

test2 = apply_event_factor(generic_hh, standard_events)
test2

sns.set()
sns.lineplot(x=test2.ds, y=test2.yhat)
plt.show()

