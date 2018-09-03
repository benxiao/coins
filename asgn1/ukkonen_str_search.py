from ukkonen import SuffixTree, mark_leaves, Edge, Node

# early proto type
# def find_pattern(node, text, pattern, length):
#     edge = node.edges.get(pattern[length])
#     if edge:
#         if edge.length() < (len(pattern) - length):
#             for (i, j) in enumerate(range(edge.start, edge.end)):
#                 if pattern[i] != text[j]:
#                     return None
#             return find_pattern(edge.nextNode, text, pattern, length+edge.length())
#         else:
#             for (j, i) in enumerate(range(length, len(pattern))):
#                 if pattern[i] != text[edge.start + j]:
#                     return None
#             if edge.is_leaf():
#                 return edge
#             return edge.nextNode
#     return None


def find_pattern_with_hammingdist(node, edge_chr, edge_i, text, pattern, length, diff, result):
    # base case
    if len(pattern) == length:
        edge = node.edges.get(edge_chr)
        if edge:
            if edge.is_leaf():
                result.append((edge, diff))
            else:
                result.append((edge.nextNode, diff))
        else:
            result.append((node, diff))
        # we need to terminate here
        return

    # exact match
    edge = node.edges.get(edge_chr)
    if edge:
        # we are run out of text
        if edge.start + edge_i == len(text):
            return

        if text[edge.start + edge_i] == pattern[length]:
            if edge_i + 1 < edge.length():
                find_pattern_with_hammingdist(node, edge_chr, edge_i+1, text, pattern, length+1, diff, result)
            else:
                ch = pattern[length+1] if length+1 < len(pattern) else None
                find_pattern_with_hammingdist(edge.nextNode, ch, 0, text, pattern, length+1, diff, result)
        else:
            # we have a mismatch on the edge
            if diff > 0:
                if edge_i + 1 < edge.length():
                    find_pattern_with_hammingdist(node, edge_chr, edge_i+1, text, pattern, length+1, diff-1, result)
                else:
                    ch = pattern[length + 1] if length + 1 < len(pattern) else None
                    find_pattern_with_hammingdist(edge.nextNode, ch, 0, text, pattern, length+1, diff-1, result)

    # mismatch at a node
    if edge_i == 0:
        for e_chr in node.edges:
            if e_chr != edge_chr:
                edge = node.edges.get(e_chr)
                if diff > 0:
                    if edge_i + 1 < edge.length():
                        find_pattern_with_hammingdist(node, e_chr, edge_i+1, text, pattern, length+1, diff-1, result)
                    else:
                        ch = pattern[length + 1] if length + 1 < len(pattern) else None
                        find_pattern_with_hammingdist(edge.nextNode, ch, 0, text, pattern, length+1, diff-1, result)


def find_ends(node, lst):
    for e in node.edges:
        edge = node.edges[e]
        if edge.is_leaf():
            lst.append(edge.suffix_id)
        else:
            find_ends(edge.nextNode, lst)


def indexes_with_hammingdist(text, pattern, diff):
    st = SuffixTree()
    for ch in text:
        st.add_char(ch)
    mark_leaves(st.root, len(text), 0)
    nodes_or_edges = []
    find_pattern_with_hammingdist(st.root, pattern[0], 0, text, pattern, 0, diff, nodes_or_edges)
    result = []
    # print(nodes_or_edges)
    for (item, allowance) in nodes_or_edges:
        if isinstance(item, Edge):
            result.append((item.suffix_id, diff-allowance))
        else:
            tmp = []
            find_ends(item, tmp)
            for t in tmp:
                result.append((t, diff-allowance))
    return result


if __name__ == '__main__':
    text = "abcabcabcd$"
    #text = 'abcabcabc$'
    pattern = "afcf"
    st = SuffixTree()
    for ch in text:
        st.add_char(ch)
    mark_leaves(st.root, len(text), 0)
    result = []
    print(indexes_with_hammingdist(text, pattern, 2))
    # print(indexes(st.root, text, pattern))
    # #print(st.root)


