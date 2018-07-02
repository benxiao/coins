import pandas as pd
import matplotlib.pyplot as plt
import operator
from candlestick import *


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


if __name__ == '__main__':
    columns = ['open', 'close', 'lowest', 'highest']
    df = pd.read_csv('btc_daily.csv', index_col=0)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df[columns] = df[columns].astype(np.float64)
    df['ma200'] = df['open'].ewm(200).mean()
    fig = plt.figure(figsize=(32, 40))
    starting_year = 2013
    ending_year = 2019
    n = ending_year - starting_year
    for i, y in enumerate(range(starting_year, ending_year)):
        ax = plt.subplot(n, 1, i+1)
        yearly_df = aggregate_to_2d(df[df['date'].dt.year == y])
        plot_candlestick(
            ax, yearly_df['date'].map(lambda x: f"{x.year}-{x.month}-{x.day}"),
            yearly_df['open'], yearly_df['close'], yearly_df['lowest'], yearly_df['highest'],
            tsevery=14
        )
        ax.set_title(f"YEAR {y}")
        # plot 230 day rolling average
        ax.plot(yearly_df['date'].map(lambda x: f"{x.year}-{x.month}-{x.day}"), yearly_df['ma200'])
    plt.show()
