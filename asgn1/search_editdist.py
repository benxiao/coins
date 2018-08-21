from z_algo import zbox_search
from ed import levenshtein_distance


def get_partitions(ss, n):
    assert n < len(ss)
    pattern_length = len(pattern)
    partition_length = pattern_length // n
    partitions = []
    for i in range(n):
        partitions.append([i*partition_length, (i+1)*partition_length])
    partitions[-1][1] = pattern_length
    return partitions


if __name__ == '__main__':
    text = "abdyabxdcyabcdz"
    pattern = "abcd"
    pattern_length = len(pattern)
    partitions = get_partitions(pattern, 2)
    result = []
    for i, j in partitions:
        ps = pattern[i:j]
        hits = zbox_search(text, ps)
        for h in hits:
            i+1
            # mismatch = 0
            # # verify string segment before partition
            # if i > 0:
            #     for k in range(i):
            #         if text[h-i+k] != pattern[k]:
            #             mismatch += 1
            # # verify string segment after partition
            # if j < pattern_length:
            #     for k in range(j, pattern_length):
            #         if pattern[k] != text[h+k]:
            #             mismatch += 1
            #
            # if mismatch < 2:
            #     result.append((h-i, mismatch))

        result = list(set(result))
        result.sort(key=lambda x: x[0])
    for i, mis in result:
        print(i+1, mis)
