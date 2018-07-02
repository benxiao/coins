from candlestick import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_df(fn):
    df = pd.read_csv(fn, index_col=0)
    # print(df)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    df.astype(np.float64)
    df.sort_index(0)
    return df


if __name__ == '__main__':
    btc_df = get_df("bitcoin_daily.csv")
    btc_df = btc_df['2018-03-01':]
    ada_df = get_df("cardano_daily.csv")
    ada_df = ada_df['2018-03-01':]
    btc_df = btc_df / btc_df.head(10)['open'].mean()
    ada_df = ada_df / ada_df.head(10)['open'].mean()
    fig = plt.figure(figsize=(20, 15))
    ax = plt.subplot(1, 1, 1)
    plot_candlestick(ax, btc_df.index.map(lambda x: f"{x.year}-{x.month}-{x.day}"),
                     np.log10(btc_df['open']),
                     np.log10(btc_df['close']),
                     np.log10(btc_df['lowest']),
                     np.log10(btc_df['highest']),
                     tsevery=30)

    plot_candlestick(ax, ada_df.index.map(lambda x: f"{x.year}-{x.month}-{x.day}"),
                     np.log10(ada_df['open']),
                     np.log10(ada_df['close']),
                     np.log10(ada_df['lowest']),
                     np.log10(ada_df['highest']),
                     tsevery=30, bull='blue', bear='purple')
    plt.show()
