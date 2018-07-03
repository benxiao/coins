import numpy as np
import datetime
from pandas import Series, DataFrame
import pandas as pd


def plot_candlestick(_ax, ts_labels, _open, close, lowest, highest, tsevery=5, bull='g', bear='r'):
    index = np.arange(len(ts_labels))
    index = index + 0.5
    candle_bottom = np.min(np.vstack((_open, close)), axis=0)
    candle_top = np.max(np.vstack((_open, close)), axis=0)
    candle_length = candle_top - candle_bottom
    candle_max_stick = (highest - candle_top) / 2
    candle_color = close > _open
    candle_min_stick = (candle_bottom - lowest) / 2
    _ax.bar(index, candle_length, 1, bottom=candle_bottom, alpha=0.6, color=[bull if c else bear for c in candle_color])
    for pos, top, bottom, max_stick, min_stick, color in \
            zip(index, candle_top, candle_bottom, candle_max_stick, candle_min_stick, candle_color):
        _ax.errorbar(pos, top + max_stick, max_stick, lw=2, capsize=2, capthick=2, color=bull if color else bear)
        _ax.errorbar(pos, bottom - min_stick, min_stick, lw=2, capsize=2, capthick=2, color=bull if color else bear)
    _ax.set_xticks(index[::tsevery])
    _ax.set_xticklabels(ts_labels[::tsevery], rotation=45)
    _ax.grid(axis='y', linestyle='dashed', linewidth=2)


def get_df(fn):
    df = pd.read_csv(fn, index_col=0)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    df = df.astype(np.float64)
    df['ma200'] = df['open'].ewm(200).mean()
    df['ma26'] = df['open'].ewm(26).mean()
    df['ma12'] = df['open'].ewm(12).mean()
    return df


def fill_to_end_of_year(df):
    last = df.tail(1).index[0]
    year = last.year
    end = datetime.datetime(year+1, 1, 1)
    index_lst = []
    i = 1
    while last + datetime.timedelta(days=i) < end:
        index_lst.append(last + datetime.timedelta(days=i))
        i += 1

    filler = np.empty((len(index_lst), len(df.columns)))
    rest = DataFrame(filler, columns=df.columns)
    rest.index = index_lst
    return np.concat((df, rest))


def aggregated_to(df, by):
    def _agg(x):
        date = x.head(1).index.values[0]
        open = x.head(1)['open'].values[0]
        close = x.tail(1)['close'].values[0]
        ma200 = x.head(1)['ma200'].values[0]
        ma12 = x.head(1)['ma12'].values[0]
        ma26 = x.head(1)['ma26'].values[0]
        hi = x['highest'].max()
        lo = x['lowest'].min()
        volume = x['volume'].mean()
        return Series(
            {
                "date": date,
                "open": open,
                "close": close,
                "highest": hi,
                "lowest": lo,
                "ma200": ma200,
                "ma26": ma26,
                "ma12": ma12,
                "volume": volume
            }
        )
    # implement weekly
    result = df.groupby(by, sort=False).apply(_agg)
    # print("result:", result)
    return result.set_index('date')


def aggregate_to_2d(df):
    return aggregated_to(df, df.index.map(lambda x: x.dayofyear // 2))


def aggregate_to_3d(df):
    return aggregated_to(df, df.index.map(lambda x: x.dayofyear // 3))


def aggregate_to_weekly(df):
    return aggregated_to(df, df.index.map(ugly_fix))


def aggregate_to_fortnightly(df):
    return aggregated_to(df, df.index.map(ugly_fix).map(lambda x: x // 2))


def aggregate_to_monthly(df):
    return aggregated_to(df, df.index.map(lambda x: f"{x.year}-{x.month}"))


def ugly_fix(x):
    if x.month == 12 and x.week == 1:
        return 53
    if x.month == 1 and x.week in (52, 53):
        return 0
    return x.week


def datestr(d):
    if not isinstance(d, (datetime.datetime, datetime.date)):
        raise TypeError()
    return f"{d.year}-{str(d.month).zfill(2)}-{str(d.day).zfill(2)}"