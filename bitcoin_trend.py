import pandas as pd
import matplotlib.pyplot as plt
import operator
from candlestick import *

df = get_df('bitcoin_daily.csv')
print(df.head())
print(df.columns)
starting_year = 2013
ending_year = 2019
n = ending_year - starting_year
fig = plt.figure(figsize=(40, 50))
for (i, y) in enumerate(range(starting_year, ending_year)):
    ax = plt.subplot(n, 1, i+1)
    yearly_df = df[str(y)]
    yearly_df = aggregate_to_3d(yearly_df)
    plot_candlestick(
        ax, yearly_df.index.map(lambda x: f"{x.year}-{x.month}-{x.day}"),
        yearly_df['open'], yearly_df['close'], yearly_df['lowest'], yearly_df['highest'], tsevery=14
    )
    ax.set_title(f"YEAR {y}")
    # plot 230 day rolling average
    ax.plot(yearly_df.index.map(lambda x: f"{x.year}-{x.month}-{x.day}"), yearly_df['ma200'], linewidth=3)
    ax.plot(yearly_df.index.map(lambda x: f"{x.year}-{x.month}-{x.day}"), yearly_df['ma12'],
            linestyle='dotted', color='cyan', linewidth=3)
    ax.plot(yearly_df.index.map(lambda x: f"{x.year}-{x.month}-{x.day}"), yearly_df['ma26'],
            linestyle='dotted', color='red', linewidth=3)
plt.show()
