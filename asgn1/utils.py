def get_partitions(ss, n):
    assert n < len(ss)
    pattern_length = len(ss)
    partition_length = pattern_length // n
    partitions = []
    for i in range(n):
        partitions.append([i*partition_length, (i+1)*partition_length])
    partitions[-1][1] = pattern_length
    return partitions