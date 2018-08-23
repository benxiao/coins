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
        self.link = None

    def __contains__(self, item):
        return item in self.nodes

    def __str__(self):
        return f"nodes: {self.nodes}, link:{id(self.link)}"
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
    source = "xyzxyaxyz$"
    source_length = len(source)

    root = Node()
    root.link = root
    end = -1
    active_node = root
    active_length = 0
    active_edge = -1 # should be a number
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
                    # we increment and decrement active edge
                    # no more i shit
                    active_edge = 0
                    active_length = 1
                    break # break out the loop

                # the following code is wrong
                # ToDo replace it
                # # rule2a extension
                # # if the edge is not present
                else:
                    active_node.nodes[current] = Edge(i, -1)
                    remaining -= 1
            else:
                #
                edge = active_node.nodes.get(source[active_edge])
                # which means it is not a leaf edge
                if edge.end != -1 and edge.end == edge.start + active_length:
                    active_node = edge.nextNode
                    active_length = 0
                    active_edge = edge.end
                    edge = edge.nextNode.nodes.get(current)

                if edge and source[edge.start + active_length] == current:
                    active_length += 1
                    break

                else:
                    # we are breaking at a node
                    if active_length == 0 and active_node is not root:
                        current_node = active_node
                        while current_node != root:
                            current_node.nodes[current] = Edge(i, -1)
                            remaining -= 1
                            current_node = current_node.link
                    else:
                        if active_node is root:
                            # we are breaking at the middle of an edge
                            # we need to have some check t
                            old_edge_end = edge.end
                            edge.end = edge.start + active_length
                            oldNode = edge.nextNode
                            newNode = Node()
                            edge.nextNode = newNode
                            # point the newNode to root by default
                            newNode.link = root
                            newEdge = Edge(edge.end, old_edge_end)
                            newEdge.nextNode = oldNode
                            newNode.nodes[source[newEdge.start]] = newEdge
                            newEdge2 = Edge(i, -1)
                            newNode.nodes[source[newEdge2.start]] = newEdge2

                            # save the reference of prevNode in case of future assignments
                            prevNode = newNode
                            # be super careful with these
                            remaining -= 1
                            active_edge += 1
                            if active_node is root:
                                active_length -= 1
                            active_node = active_node.link

                            # when we move the active node from root to another node, we need to reset the active_length to 0
                            # so just watch the active length is not enough
                            # ToDo

                            #
                            #
                            while active_length: # this is the wrong condition
                                # we need to walk down the edge to find the corresponding we are looking for
                                # simpified now but will have to be changed later
                                edge = active_node.nodes[source[active_edge]]
                                print(active_length)
                                print("edge:", edge)

                                # same old same old
                                old_edge_end = edge.end
                                edge.end = edge.start + active_length
                                oldNode = edge.nextNode
                                newNode = Node()
                                edge.nextNode = newNode
                                # point the newNode to root by default
                                newNode.link = root
                                newEdge = Edge(edge.end, old_edge_end)
                                newEdge.nextNode = oldNode
                                newNode.nodes[source[newEdge.start]] = newEdge
                                newEdge2 = Edge(i, -1)
                                newNode.nodes[source[newEdge2.start]] = newEdge2

                                remaining -= 1
                                active_edge += 1

                                # only when the active node is
                                active_length -= 1
                                active_node = active_node.link

                                prevNode.link = newNode

                        else:
                            # we are breaking at the middle of an edge
                            # we need to have some check t
                            old_edge_end = edge.end
                            edge.end = edge.start + active_length
                            oldNode = edge.nextNode
                            newNode = Node()
                            edge.nextNode = newNode
                            # point the newNode to root by default
                            newNode.link = root
                            newEdge = Edge(edge.end, old_edge_end)
                            newEdge.nextNode = oldNode
                            newNode.nodes[source[newEdge.start]] = newEdge
                            newEdge2 = Edge(i, -1)
                            newNode.nodes[source[newEdge2.start]] = newEdge2

                            # save the reference of prevNode in case of future assignments
                            prevNode = newNode
                            # be super careful with these
                            remaining -= 1
                            active_edge += 1
                            if active_node is root:
                                active_length -= 1
                            active_node = active_node.link

                            # when we move the active node from root to another node, we need to reset the active_length to 0
                            # so just watch the active length is not enough
                            # ToDo

                            #
                            #
                            while active_node is not root:  # this is the wrong condition
                                # we need to walk down the edge to find the corresponding we are looking for
                                # simpified now but will have to be changed later
                                edge = active_node.nodes[source[active_edge]]
                                print(active_length)
                                print("edge:", edge)

                                # same old same old
                                old_edge_end = edge.end
                                edge.end = edge.start + active_length
                                oldNode = edge.nextNode
                                newNode = Node()
                                edge.nextNode = newNode
                                # point the newNode to root by default
                                newNode.link = root
                                newEdge = Edge(edge.end, old_edge_end)
                                newEdge.nextNode = oldNode
                                newNode.nodes[source[newEdge.start]] = newEdge
                                newEdge2 = Edge(i, -1)
                                newNode.nodes[source[newEdge2.start]] = newEdge2

                                remaining -= 1
                                active_edge += 1

                                # only when the active node is
                                if active_node is root:
                                    active_length -= 1
                                active_node = active_node.link

                                prevNode.link = newNode



                    # finally if it is not present on root, add it to the root
                    if not active_node.nodes.get(source[i]):
                        active_node.nodes[source[i]] = Edge(i, -1)
                        active_length = 0
                        remaining -= 1

                        # hopefully remaining is 0
                        # can we check it as an invariant?
                        print(f"remaing is {remaining}")

                    # we are break at a node # following the suffix links




    # source_length = len(source)
    # for i in range(1, source_length+1):
    #     for j in range(i):
    #         fst_chr = source[j]
    #         grow(root, source, j, i)

    print(root)
    print("active_length:", active_length)
    print("active_edge:", active_edge)
