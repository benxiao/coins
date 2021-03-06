import os
import pandas as pd
import matplotlib.pyplot as plt


import stats

data_dir = 'data/eth'
fig = plt.figure(figsize=(30, 10))
ax = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

fn = "ATABTC_f_2018-02-11 04:35:00_t_2018-02-27 04:00:00.csv"

df = pd.read_csv(fn, index_col=0)
df = df.reset_index(drop=True)
df['time'] = pd.to_datetime(df['time'])
#print(df)

begin, finish = 0, 10000
ax.plot(range(finish-begin), df['open'][begin: finish])
ax.grid(color='r', axis='y')
#ax.set_xticks(list(range(begin, finish, 10)))

data = list(df['open'][:finish-begin])
segment0 = 10
segment1 = 10
gap = 5
lst = [1] * (segment0 + segment1 + gap)
for i in range(finish-begin-segment0-segment1-gap):
    part1 = data[i:i+segment0]
    part2 = data[i+segment0+gap: i+segment0+gap+segment1]
    z = stats.zcoreForTwoDistributions(part1, part2)
    s = stats.surprise(z, _type=stats.TestType.GreaterThan)
    # print("part1:", part1)
    # print("part2:", part2)
    lst.append(s)


ax2.plot(range(finish-begin), [1-x for x in lst], color='red')

plt.show()
