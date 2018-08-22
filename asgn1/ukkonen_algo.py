class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.nextNode = None

    def __str__(self):
        return f"Edge({self.start},{self.end}) : {self.nextNode}"

    __repr__ = __str__


class Node:
    def __init__(self):
        self.nodes = {}

    def __contains__(self, item):
        return item in self.nodes

    def __str__(self):
        return str(self.nodes)
    __repr__ = __str__


def grow(root, source, start_index, end_index):
    print("start_index: ", start_index, "end_index: ", end_index)
    print(f"substring:({source[start_index:end_index]})")
    edge = root.nodes.get(source[start_index])
    if not edge:
        print("apply rule 2a")
        root.nodes[source[start_index]] = Edge(start_index, end_index)
        print(root)
        print(end='\n' * 2)
        return
    delta = 0
    while edge.start + delta < edge.end and start_index + delta < end_index:
        if source[edge.start+delta] != source[start_index+delta]:
            print("apply rule 2b")
            newNode = Node()
            newEdgeA = Edge(edge.start+delta, edge.end)
            edge.end = edge.start+delta
            newEdgeA.nextNode = edge.nextNode
            edge.nextNode = newNode
            newEdgeB = Edge(start_index+delta, end_index)
            newNode.nodes[source[newEdgeA.start]] = newEdgeA
            newNode.nodes[source[newEdgeB.start]] = newEdgeB
            print(root)
            print(end='\n' * 2)
            return

        delta += 1

    if start_index + delta == end_index:
        print("apply rule 3")
        print(root)
        print(end='\n' * 2)

    elif edge.start + delta == edge.end:
        if start_index + delta < end_index and edge.nextNode is not None:
            grow(edge.nextNode, source, start_index+delta, end_index)
        else:
            edge.end = end_index
            print("apply rule 1")
            print(root)
            print(end='\n' * 2)


if __name__ == '__main__':
    source = "abcabc"
    source_length = len(source)
    root = Node()
    end = -1
    active_node = root
    active_length = 0
    active_edge = 0 # should be a number
    remaining = 0
    for i in range(source_length):
        end = i
        remaining += 1
        while remaining:
            current = source[i]

            if active_length == 0:
                edge = active_node.nodes.get(current)
                # rule 3
                if edge:
                    active_edge = current
                    active_length = 1
                    break # break out the loop

                # rule2a extension
                # if the edge is not present
                else:
                    active_node.nodes[current] = Edge(i, -1)
                    remaining -= 1
            else:
                edge = active_node.nodes.get(active_edge)
                if source[edge.start + active_length] == current:
                    active_length += 1
                    break

                else:
                    # rule2b extension
                    # I hate this bits :(
                    pass

    # source_length = len(source)
    # for i in range(1, source_length+1):
    #     for j in range(i):
    #         fst_chr = source[j]
    #         grow(root, source, j, i)

    print(root)
    print(active_length)
    print(active_edge)
