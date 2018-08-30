import random
import navie
from ukkonen import SuffixTree, dfs
random.seed(42)

for k in range(5):
    text = "suffix_trees_and_bwt_are_related$"
    text = ''.join(random.choice("abcd") for _ in range(100000)) + '$'
    navie_sa, navie_bwt = navie.get_bwt(text)
    st = SuffixTree()
    for i in range(len(text)):
        st.add_char(text[i])
    lst = []
    dfs(st.root, lst, len(text), 0)
    # print("suffix array: ", lst)
    # print("navie  array: ", navie_sa)
    text_length = len(text)
    # print("".join(text[i] for i in lst))
    # print("".join(text[(i + text_length - 1) % text_length] for i in lst))
    if navie_sa == lst:
        print(f"str {k} match")
    else:
        raise ValueError("your code is broken!")
