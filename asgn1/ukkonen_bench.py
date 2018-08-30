from ukkonen import SuffixTree
from navie import get_bwt
import random
import time

"""
n:  10 duration:  0.00023412704467773438
n:  100 duration:  0.002816915512084961
n:  1000 duration:  0.0201108455657959
n:  10000 duration:  0.25030517578125
n:  100000 duration:  3.1776750087738037
n:  1000000 duration:  39.950459003448486
"""

for n in [10, 100, 1000, 10000, 100000, 1000000]:
    st = SuffixTree()
    ss = "".join(random.choice("abcd") for _ in range(n))
    start = time.time()
    # get_bwt(ss)
    for ch in ss:
        st.add_char(ch)
    duration = time.time() - start
    print("n: ", n, "duration: ", duration)
