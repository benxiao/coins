def levenshtein_distance(s1, s2):
    m = len(s1) + 1
    n = len(s2) + 1
    tbl = [[0] * n for _ in range(m)]
    for i in range(n):
        tbl[0][i] = i
    for i in range(m):
        tbl[i][0] = i
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            tbl[i][j] = min(tbl[i][j - 1] + 1, tbl[i - 1][j] + 1, tbl[i - 1][j - 1] + cost)

    return tbl[m - 1][n - 1]


def levenshtein_distance_lt_1(s1, s2):
    m, n = len(s1), len(s2)
    # two strings can only be one character length apart
    if (abs(m-n)) > 1:
        print(s1, s2, "at least two characters apart")
        return False, None
    count = 0
    i, j = 0, 0
    while i < m and j < n:
        if s1[i] != s2[j]:
            if count > 0:
                return False, None
            else:
                count += 1
                if m > n:
                    i += 1
                elif m < n:
                    j += 1
                else:
                    j += 1
                    i += 1
        else:
            i += 1
            j += 1
    return True, count


if __name__ == '__main__':
    print(levenshtein_distance("abc", "ac"))
    print(levenshtein_distance_lt_1("abc", "ab"))
    print(levenshtein_distance_lt_1("ab", "abc"))
    print(levenshtein_distance_lt_1("ac", "abc"))
    print(levenshtein_distance_lt_1("abc", "ac"))
    print(levenshtein_distance_lt_1("abc", "abcde"))
    print(levenshtein_distance_lt_1("xd", "cd"))
