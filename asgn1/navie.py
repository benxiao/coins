from utils import StrProxy


def get_bwt(text):
    text_length = len(text)
    result = [StrProxy(text, i, text_length) for i in range(text_length)]
    suffix_array = sorted(list(range(text_length)), key=lambda x: result[x])
    bwt_str = "".join(text[(i + text_length - 1) % text_length] for i in suffix_array)
    return suffix_array, bwt_str


def diff(str0, str1):
    return sum(c0 != c1 for c0, c1 in zip(str0, str1))


def navie_search(text, pat, n):
    pat_length = len(pat)
    diffs = (diff(StrProxy(text, i, i+pat_length), pat) for i in range(len(text)-pat_length+1))
    hits = ((i, d) for i, d in enumerate(diffs) if d <= n)
    result = list(hits)
    #print(result)
    return result


if __name__ == '__main__':
    # text = "suffix_trees_and_bwt_are_related$"
    # sa, bwt = get_bwt(text)
    # s0 = StrProxy("abcd", 0, 4)
    # s1 = StrProxy("abcd", 1, 4)
    # # print(s0)
    # # print(s1)
    # # print(s1 < s0)
    # # print(s0 < s1)
    #
    # print("result:")
    # print("indexes:", sa)
    # print("bwt:", bwt)
    print(navie_search("abcabcabc", "abb", 1))
