def get_bwt(text):
    text_length = len(text)
    result = [text[i:] for i in range(text_length)]
    suffix_array = sorted(list(range(text_length)), key=lambda x: result[x])
    bwt_str = "".join(text[(i + text_length - 1) % text_length] for i in suffix_array)
    return suffix_array, bwt_str

def diff(str1, str2):
    if len(str1) != len(str2):
        raise ValueError("two strings have unequal length!")
    return sum([c0 != c1 for c0, c1 in zip(str1, str2)])




if __name__ == '__main__':
    sa, bwt = get_bwt("suffix_trees_and_bwt_are_related$")
    print("result:")
    print("indexes:", sa)
    print("bwt:", bwt)