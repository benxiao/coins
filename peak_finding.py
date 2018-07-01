import pandas as pd
from pandas import Series
import matplotlib.pyplot as plt
import numpy as np
import operator
import peakutils


def find_extremes(prices, n=25, method='max'):
    cmp = operator.ge if method == 'max' else operator.lt
    lst = []
    for i in range(n, len(prices) - n):
        before_i = prices[i - n: i]
        after_i = prices[i + 1: i + n + 1]
        if all(cmp(prices[i], p) for p in before_i + after_i):
            lst.append(i)
        # find n after p
    return lst


def plot_candlestick(_ax, ts_labels, _open, close, lowest, highest, tsevery=5):
    index = np.arange(len(ts_labels))
    index = index + 0.5
    candle_bottom = np.min(np.vstack((_open, close)), axis=0)
    candle_top = np.max(np.vstack((_open, close)), axis=0)
    candle_length = candle_top - candle_bottom
    candle_max_stick = (highest - candle_top) / 2
    candle_color = close > _open
    candle_min_stick = (candle_bottom - lowest) / 2
    _ax.bar(index, candle_length, 1, bottom=candle_bottom, alpha=0.6, color=['g' if c else 'r' for c in candle_color])
    for pos, top, bottom, max_stick, min_stick, color in \
            zip(index, candle_top, candle_bottom, candle_max_stick, candle_min_stick, candle_color):
        _ax.errorbar(pos, top + max_stick, max_stick, lw=2, capsize=2, capthick=2, color='g' if color else 'r')
        _ax.errorbar(pos, bottom - min_stick, min_stick, lw=2, capsize=2, capthick=2, color='g' if color else 'r')
    _ax.set_xticks(index[::tsevery])
    _ax.set_xticklabels(ts_labels[::tsevery], rotation=45)
    _ax.grid(axis='y', linestyle='dashed', linewidth=2)


def aggregated_to(df, by):
    def _agg(x):
        # print(x)
        x = x.sort_values('date')
        date = x.head(1)['date'].values[0]
        open = x.head(1)['open'].values[0]
        close = x.tail(1)['close'].values[0]
        hi = x['highest'].max()
        lo = x['lowest'].min()
        return Series(
            {
                "date": date,
                "open": open,
                "close": close,
                "highest": hi,
                "lowest": lo
            }
        )
    # implement weekly
    return df.groupby(by, sort=False).apply(_agg)


# def aggregated_to_2d(df):
#     return aggregated_to(df, lambda x: f"{x.year}-{x.month}-{x.day // 2}")

def aggregate_to_weekly(df):
    return aggregated_to(df, df['date']
                         .map(ugly_fix)
                         )


def aggregate_to_fortnightly(df):
    return aggregated_to(df, df['date'].map(ugly_fix).map(lambda x: x // 2))


def ugly_fix(x):
    if x.month == 12 and x.week == 1:
        return 53
    if x.month == 1 and x.week in (52, 53):
        return 0
    return x.week


if __name__ == '__main__':
    columns = ['open', 'close', 'lowest', 'highest']
    df = pd.read_csv('btc_daily.csv', index_col=0)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df[columns] = df[columns].astype(np.float64)
    fig = plt.figure(figsize=(16, 40))
    n = 2019 - 2014
    for i, y in enumerate(range(2014, 2019)):
        ax = plt.subplot(n, 1, i+1)
        yearly_df = aggregate_to_fortnightly(df[df['date'].dt.year == y])
        plot_candlestick(
            ax, yearly_df['date'].map(lambda x: f"{x.year}-{x.month}-{x.day}"),
            yearly_df['open'], yearly_df['close'], yearly_df['lowest'], yearly_df['highest']
        )
    plt.show()
