from candlestick import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

scale_transformer = lambda x: x
duration_transformer = aggregate_to_2d


btc_df = get_df("ethereum_daily.csv")
btc_df = btc_df['2017-11-01':]
ada_df = get_df("stellar_daily.csv")
ada_df = ada_df['2017-11-01':]
btc_df = duration_transformer(btc_df) / btc_df.head(10)['open'].mean()
ada_df = duration_transformer(ada_df) / ada_df.head(10)['open'].mean()
fig = plt.figure(figsize=(20, 15))

ax = plt.subplot(1, 1, 1)
plot_candlestick(ax, btc_df.index.map(lambda x: f"{x.year}-{x.month}-{x.day}"),
                 scale_transformer(btc_df['open']),
                 scale_transformer(btc_df['close']),
                 scale_transformer(btc_df['lowest']),
                 scale_transformer(btc_df['highest']),
                 tsevery=30)

plot_candlestick(ax, ada_df.index.map(lambda x: f"{x.year}-{x.month}-{x.day}"),
                 scale_transformer(ada_df['open']),
                 scale_transformer(ada_df['close']),
                 scale_transformer(ada_df['lowest']),
                 scale_transformer(ada_df['highest']),
                 tsevery=30, bull='blue', bear='purple')
plt.show()
