import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm

data = sm.datasets.co2.load_pandas()


y = data.data
print(y)
print()
print()
print()
print()
# The 'MS' string groups the data in buckets by start of the month
y = y['co2'].resample('MS').mean()

# The term bfill means that we use the value before filling in missing values
y = y.fillna(y.bfill())
print(y)
mod = sm.tsa.statespace.SARIMAX(y,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)


results = mod.fit()

pred_uc = results.get_forecast(steps=10)
print(pred_uc.predicted_mean)

date_rng = pd.date_range(start='1/2018', end='08/2018', freq='m')
print(date_rng)
print(len(date_rng))