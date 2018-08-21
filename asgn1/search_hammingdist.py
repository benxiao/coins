from z_algo import zbox_search
from utils import get_partitions


if __name__ == '__main__':
    text = "bbcaefadcabcpqr"
    pattern = "abc"
    pattern_length = len(pattern)
    partitions = get_partitions(pattern, 2)
    result = []
    for i, j in partitions:
        ps = pattern[i:j]
        hits = zbox_search(text, ps)
        for h in hits:
            mismatch = 0
            # verify string segment before partition
            if i > 0:
                for k in range(i):
                    if text[h-i+k] != pattern[k]:
                        mismatch += 1
            # verify string segment after partition
            if j < pattern_length:
                for k in range(j, pattern_length):
                    if pattern[k] != text[h+k]:
                        mismatch += 1
            if mismatch < 2:
                result.append((h-i, mismatch))

    result = list(set(result))
    result.sort(key=lambda x: x[0])
    for i, mis in result:
        print(i+1, mis)















