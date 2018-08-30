from uf import UnionFind

edges = [
    (1, 3, 3),
    (1, 5, 6),
    (2, 4, 9),
    (2, 4, 8),
    (4, 5, 7)
]


if __name__ == '__main__':
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

    print(trees)
