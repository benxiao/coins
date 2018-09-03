def get_partitions(ss, n):
    assert n < len(ss)
    pattern_length = len(ss)
    partition_length = pattern_length // n
    partitions = []
    for i in range(n):
        partitions.append([i*partition_length, (i+1)*partition_length])
    partitions[-1][1] = pattern_length
    return partitions


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