import os
import pandas as pd
import matplotlib.pyplot as plt


import stats

data_dir = 'data/eth'
fig = plt.figure(figsize=(30, 10))
ax = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

fn = "eth/ETHBTC_f_2018-04-30 02:01:00_t_2018-06-06 15:00:00.csv"

df = pd.read_csv(fn, index_col=0)
df = df.reset_index(drop=True)
df['time'] = pd.to_datetime(df['time'])
#print(df)

begin, finish = 1500, 10000
ax.plot(range(finish-begin), df['open'][begin: finish])
#ax.set_xticks(list(range(begin, finish, 10)))

data = list(df['open'][:finish-begin])
segment = 25
gap = 15
lst = [1] * (segment * 2 + gap)
for i in range(finish-begin-2*segment-gap):
    part1 = data[i:i+segment]
    part2 = data[i+segment+gap: i+segment*2+gap]
    z = stats.zcoreForTwoDistributions(part1, part2)
    s = stats.surprise(z, _type=stats.TestType.LessThan)
    lst.append(s)


ax2.plot(range(finish-begin),[ x for x in lst],color='green')
#ax2.plot(range(finish-begin), [1-x for x in lst1],color='red')
#ax2.set_xticks(list(range(0, finish-begin, 10)))
plt.show()