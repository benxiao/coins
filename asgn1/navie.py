class StrProxy:

    __slots__ = ['text', 'start', 'end']
    def __init__(self, text, start, end):
        self.text = text
        assert end > start
        assert end <= len(self.text)

        self.start = start
        self.end = end

    def __str__(self):
        return self.text[self.start: self.end]

    __repr__ = __str__

    def __len__(self):
        return self.end - self.start

    def __iter__(self):
        for i in range(self.start, self.end):
            yield self.text[i]

    def __lt__(self, other):
        for ch0, ch1 in zip(self, other):
            if ch0 < ch1:
                return True
            if ch0 > ch1:
                return False
        return len(self) < len(other)

    def __eq__(self, other):
        if len(self) != len(other):
            return False

        for ch0, ch1 in zip(self, other):
            if ch0 != ch1:
                return False
        return True


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
    hits = (i for i, d in enumerate(diffs) if d <= n)
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
    print(navie_search("abcabcabc", "abc", 1))
