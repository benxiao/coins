LARGE = float("inf")

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.nextNode = None

    def __str__(self):
        return f"Edge({self.start},{self.end})::{self.nextNode}"

    def length(self):
        if self.is_leaf():
            return LARGE
        return self.end - self.start

    def is_leaf(self):
        return self.end == -1

    __repr__ = __str__


class Node:
    def __init__(self, _id):
        self._id = _id
        # root node has length 0
        self.length = 0
        self.edges = {}
        self.link = None

    def __str__(self):
        return f"[node<{self.get_id()}> link<{self.link.get_id() if self.link else None}>: {self.edges}]"

    def get_id(self):
        return self._id

    __repr__ = __str__


class SuffixTree:
    def __init__(self):
        self.text = []
        self.id = 0

        self.root = Node(self._get_id())
        self.root.link = self.root

        self.active_node = self.root
        self.active_length = 0
        self.active_edge = -1
        self.prevNode = None

        self.remaining = 0

    def __str__(self):
        return str(self.root)

    def _get_id(self):
        old = self.id
        self.id += 1
        return old

    def display_state(self):
        print("text: ", "".join(self.text))
        print("text: ", self.text)
        print("iteration: ", len(self.text) - 1)
        print("tree:", self.root)
        print("active_node: ", self.active_node.get_id())
        print("active_edge:", self.active_edge)
        print("active_length:", self.active_length)
        print("remainder:", self.remaining)
        print()

    def skip_walk(self, active_node, active_edge, active_length):
        edge = active_node.edges[self.text[active_edge]]
        if edge.length() > active_length:
            self.active_node = active_node
            self.active_length = active_length
            self.active_edge = active_edge
            return

        if edge.length() == active_length:
            self.active_node = edge.nextNode
            self.active_length = 0
            #self.active_edge = active_edge
            return

        self.skip_walk(edge.nextNode, active_edge + edge.length(), active_length - edge.length())

    # this method will do surgery to
    # assume the edge being split is right next the active node

    # we should leave checking for rule 3 out of this method

    def insert(self, idx):
        if self.active_length == 0:
            if self.active_node.edges.get(self.text[idx]):
                # we trigger rule 3
                # remember we will come to a early stop
                # as we match exact [j: i] position, we guarantee to match [j+1: i] position
                self.skip_walk(self.active_node, idx, 1)
                return None

            self.active_node.edges[self.text[idx]] = Edge(idx, -1)
            return self.active_node
        # we are right on the active node
        edge = self.active_node.edges[self.text[self.active_edge]]
        old_edge_end = edge.end
        edge.end = edge.start + self.active_length
        oldNode = edge.nextNode
        newNode = Node(self._get_id())
        edge.nextNode = newNode
        newNode.link = self.root
        newEdge = Edge(edge.end, old_edge_end)
        newEdge.nextNode = oldNode
        newEdge2 = Edge(idx, -1)
        newNode.edges[self.text[newEdge.start]] = newEdge
        newNode.edges[self.text[newEdge2.start]] = newEdge2
        return newNode

    def add_char(self, ch):
        self.text.append(ch)
        i = len(self.text) - 1
        self.prevNode = None
        while 1:
            if self.active_node is self.root and self.active_length == 0:
                edge = self.root.edges.get(ch)
                if not edge:
                    self.root.edges[ch] = Edge(i, -1)
                    return
            else:
                if self.active_length:
                    edge = self.active_node.edges.get(self.text[self.active_edge])
                    self.skip_walk(self.active_node, self.active_edge, self.active_length)
                else:
                    edge = self.active_node.edges.get(ch)
                    if edge:
                        self.skip_walk(self.active_node, i, self.active_length)

            if edge and text[edge.start + self.active_length] == ch:
                self.active_edge = edge.start
                self.active_length += 1
                self.remaining += 1
                self.skip_walk(self.active_node, self.active_edge, self.active_length)
                break

            while 1:
                # rule 1
                if self.active_node is self.root:
                    if self.active_length == 0:
                        break
                    new_node = self.insert(i)
                    if new_node is None:
                        # we encounter rule 3 shut down
                        self.remaining += 1
                        return
                    self.remaining -= 1
                    self.active_length -= 1
                    self.active_edge += 1
                    if self.prevNode is not None:
                        self.prevNode.link = new_node
                    self.prevNode = new_node
                    if self.active_length > 0:
                        self.skip_walk(self.active_node, self.active_edge, self.active_length)

                # rule 2
                elif self.active_node is not self.root:
                    new_node = self.insert(i)
                    if new_node is None:
                        self.remaining += 1
                        return
                    self.remaining -= 1
                    if self.prevNode is not None:
                        self.prevNode.link = new_node
                    self.prevNode = new_node
                    self.active_node = self.active_node.link

                    # skip_walk is only necessary if the active_length > 0, as the
                    # shortest length is at least 1
                    if self.active_node is not self.root and self.active_length > 0:
                        self.skip_walk(self.active_node, self.active_edge, self.active_length)
                    else:
                        # that mean we don't have a jump and we need to use remaining to walk from [j,i] -> [j+1,i] position
                        if self.active_node is self.root and self.remaining:
                            self.skip_walk(self.active_node, i - self.remaining, self.remaining)


def dfs(node, lst, text_length, length):
    if not node:
        lst.append(text_length-length)
        return

    for e in sorted(node.edges.keys()):
        edge = node.edges[e]
        edge_length = edge.length() if not edge.is_leaf() else text_length-edge.start
        dfs(edge.nextNode, lst, text_length, length+edge_length)


if __name__ == '__main__':
    import random
    import navie
    random.seed(42)
    text = "suffix trees and bwt are related$"
    # text = ''.join(random.choice("abcd") for _ in range(1000)) + '$'
    navie_sa, navie_bwt = navie.get_bwt(text)
    st = SuffixTree()
    for i in range(len(text)):
        st.add_char(text[i])
    st.display_state()
    lst = []
    dfs(st.root, lst, len(text), 0)
    print("suffix array: ", lst)
    print("navie  array: ", navie_sa)
    text_length = len(text)
    print("".join(text[i] for i in lst))
    print("".join(text[(i + text_length - 1) % text_length] for i in lst))
    print(navie_bwt)