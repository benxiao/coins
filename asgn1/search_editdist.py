from z_algo import zbox_search
from ed import levenshtein_distance_lt_1
from utils import get_partitions


if __name__ == '__main__':
    text = "abdyabxdcyabcdz"
    pattern = "abcd"
    pattern_length = len(pattern)
    first_half, second_half = get_partitions(pattern, 2)
    result = []
    i, j = first_half
    ps = pattern[i:j]

    ps2 = pattern[j:pattern_length]
    hits = zbox_search(text, ps)
    print("first half hits:", hits)
    for h in hits:
        print("hit:", h)
        # check for substitution
        print("match substitute")
        print(ps2, text[h+j: h+pattern_length])
        res, d = levenshtein_distance_lt_1(ps2, text[h+j: h+pattern_length])
        if res:
            result.append((h, d))
        # check for deletion
        print(ps2, text[h+j: h+pattern_length+1])
        res, d = levenshtein_distance_lt_1(ps2, text[h+j: h+pattern_length+1])
        if res:
            result.append((h, 1))
        # check for insertion
        print(ps2, text[h+j: h+pattern_length-1])
        res, d = levenshtein_distance_lt_1(ps2, text[h+j: h+pattern_length-1])
        if res:
            result.append((h, 1))

    i, j = second_half
    print(i, j)

    print("tt", i, j)
    ps = pattern[i:j]
    print("second half pattern:", ps)
    ps2 = pattern[:i]
    hits = zbox_search(text, ps)
    print("second half hits", hits)
    for h in hits:
        print("hit", h)
        # check for substitution
        res, d = levenshtein_distance_lt_1(ps2, text[h-i: h])
        print(ps2, text[h-i: h])
        if res:
            result.append((h-i, d))
        # check for deletion
        res, d = levenshtein_distance_lt_1(ps2, text[h-i+1: h])
        print(ps2, text[h-i+1: h])
        if res:
            result.append((h-i+1, 1))
        # check for insertion
        res, d = levenshtein_distance_lt_1(ps2, text[h-i-1: h])
        print(ps2, text[h-i-1: h])
        if res:
            result.append((h-i-1, 1))

    result = list(set(result))
    result.sort(key=lambda x: x[0])
    for i, mis in result:
        print(i+1, mis)
