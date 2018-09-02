import random
import navie
from ukkonen import SuffixTree, mark_leaves, dfs
from ukkonen_str_search import indexes_with_hammingdist
random.seed(42)
print("suffix tree test")
for k in range(5):
    text = "suffix_trees_and_bwt_are_related$"
    text = ''.join(random.choice("abcd") for _ in range(10000)) + '$'
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
print()
print("n mismatch test")
for i in range(10):
    text = "".join(random.choice("abcd") for _ in range(1000)) + "$"
    for j in range(3):
        navie_result = navie.navie_search(text, "abc", i)
        better_result = indexes_with_hammingdist(text, "abc", i)
        navie_result.sort()
        better_result.sort()
        if navie_result == better_result:
            print(f"str {i} match with {j} subs or less")
        else:
            raise ValueError("your code is broken!")




