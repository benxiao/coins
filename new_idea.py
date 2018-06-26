import coin_market_cap as cmc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('btc_daily.csv', index_col=0)
df['date'] = pd.to_datetime(df['date'])
df['open'] = df['open'].astype(np.float64)
fig = plt.figure(figsize=(12, 16))
for i, yy in enumerate(range(2013, 2019)):
    _df = df[df['date'].dt.year == yy]
    ax = plt.subplot(6, 1, i+1)
    ax.hist(_df['open'], 40)
    ax.set_title(f"year: {yy}")
plt.tight_layout()
plt.show()
