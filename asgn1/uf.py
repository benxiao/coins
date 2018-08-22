class UnionFind:
    def __init__(self, n):
        self.parent = [-1] * n

    def find(self, i):
        while self.parent[i] >= 0:
            i = self.parent[i]
        return i

    def find_path_compression(self, i):
        if self.parent[i] < 0:
            return i
        # what is this!
        self.parent[i] = self.find_path_compression(self.parent[i])
        return self.parent[i]

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            # a and b are already connected
            return
        size_a = -self.parent[root_a]
        size_b = -self.parent[root_b]

        # tree b is smaller than tree a
        if size_a >= size_b:
            self.parent[root_b] = root_a
            self.parent[root_a] = -(size_a+size_b)
        else:
            self.parent[root_a] = root_b
            self.parent[root_b] = -(size_a+size_b)
