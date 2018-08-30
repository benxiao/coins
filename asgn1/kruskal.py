from uf import UnionFind
import sys


if __name__ == '__main__':
    filename = sys.argv[1]
    edges = []
    with open(filename, 'r') as fp:
        for line in fp:
            edges.append(tuple(int(x) for x in line.strip().split(maxsplit=2)))

    edges.sort(key=lambda x: x[2], reverse=True)
    element_count = max(max(e[0] for e in edges), max(e[1] for e in edges))

    trees = []
    union_find = UnionFind(element_count+1)
    connections = element_count - 1
    while connections:
        i, j, w = edges.pop()
        while union_find.find(i) == union_find.find(j):
            i, j, w = edges.pop()
        trees.append((i, j, w))
        union_find.union(i, j)
        connections -= 1

    for i, j, l in sorted(trees, key=lambda x: x[2]):
        print(i, j, l)
