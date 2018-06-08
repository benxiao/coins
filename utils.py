import os
import pandas as pd
from datetime import timedelta


def read_multiple_csv_files(data_dir):
    lst = []
    for line in os.listdir(data_dir):
        fn = os.path.join(data_dir, line)
        _df = pd.read_csv(fn, index_col=0)
        _df['time'] = pd.to_datetime(_df['time'].astype(int) / 1000, unit='s')
        lst.append(_df)
    df = pd.concat(lst)
    return df.sort_values('time').reset_index(drop=True)



if __name__ == '__main__':
    df = read_multiple_csv_files('data/eth')
    print(df)
    start = 0
    end = len(df)
    gap = timedelta(seconds=600)
    i = 0
    while i < end-1:
        td = df['time'][i+1] - df['time'][i]
        if td > gap:
            fn = f"ETHBTC_f_{df['time'][start]}_t_{df['time'][i]}.csv"
            print(fn)
            df[start: i+1].to_csv(fn)
            start = i+1
        i += 1
    fn = f"ETHBTC_f_{df['time'][start]}_t_{df['time'][i]}.csv"
    print(fn)
    df[start: i + 1].to_csv(fn)


