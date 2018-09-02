from ukkonen import SuffixTree
from navie import get_bwt
import random
import time

"""
on  i7 4770 3.7Ghz 
Ukkonen
n:  10 duration:  5.1975250244140625e-05
n:  100 duration:  0.0013833045959472656
n:  1000 duration:  0.012046098709106445
n:  10000 duration:  0.13390183448791504
n:  100000 duration:  1.8934078216552734
n:  1000000 duration:  23.977630138397217
n:  10000000 duration:  271.77288484573364

Navie
n:  10 duration:  9.274482727050781e-05
n:  100 duration:  0.0014100074768066406
n:  1000 duration:  0.02798008918762207
n:  10000 duration:  0.35556769371032715
n:  100000 duration:  5.411811828613281
n:  1000000 duration:  66.40487694740295
n:  10000000 duration:  869.8641338348389
"""

for n in [10, 100, 1000, 10000, 100000, 1000000, 10000000]:
    st = SuffixTree()
    ss = "".join(random.choice("abcd") for _ in range(n))
    start = time.time()
    #get_bwt(ss)
    for ch in ss:
        st.add_char(ch)
    duration = time.time() - start
    print("n: ", n, "duration: ", duration)
