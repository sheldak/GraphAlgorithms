import sys

from dimacs import loadWeightedGraph


class Node:
    def __init__(self, idx):
        self.idx = idx
        self.out = set()              # set with neighbours

    def connect_to(self, v):
        self.out.add(v)


def load_graph(file_path):
    (v_num, vertices) = loadWeightedGraph(file_path)
    graph = [None] + [Node(i) for i in range(1, v_num + 1)]  # to index vertices by their number

    for (u, v, _) in vertices:
        graph[u].connect_to(v)
        graph[v].connect_to(u)

    return graph


def lex_bfs(graph):
    full_set = set()
    for i in range(2, len(graph)):
        full_set.add(i)

    queue = [full_set, {1}]
    lex_list = []

    for i in range(1, len(graph)):
        new_queue = []

        curr_v = queue[-1].pop()
        lex_list.append(curr_v)
        for s in queue:
            adj = s & graph[curr_v].out
            not_adj = s - adj

            if not_adj:
                new_queue.append(not_adj)

            if adj:
                new_queue.append(adj)

        queue = new_queue

    return lex_list


def checkLexBFS(graph, vs):
    n = len(graph)
    pi = [None] * n
    for i, v in enumerate(vs):
        pi[v] = i

    for i in range(n-1):
        for j in range(i+1, n-1):
            Ni = graph[vs[i]].out
            Nj = graph[vs[j]].out

            verts = [pi[v] for v in Nj - Ni if pi[v] < i]
            if verts:
                viable = [pi[v] for v in Ni - Nj]
                if not viable or min(verts) <= min(viable):
                    return False
    return True


def check_perfect_elimination_ordering(graph, lex_list):
    rn_v = []

    for i in range(len(lex_list)):
        curr_rn_v = set()
        parent_index = -1
        for neigh_index in range(i):
            if lex_list[neigh_index] in graph[lex_list[i]].out:
                curr_rn_v.add(lex_list[neigh_index])
                parent_index = neigh_index

        rn_v.append(curr_rn_v)

        if parent_index >= 0 and not (curr_rn_v - {lex_list[parent_index]}).issubset(rn_v[parent_index]):
            return False

    return True


def check_if_chordal(file_path):
    graph = load_graph(file_path)

    lex_list = lex_bfs(graph)

    if check_perfect_elimination_ordering(graph, lex_list):
        print(1)
    else:
        print(0)


# check_if_chordal("chordal/cycle4")
# check_if_chordal(sys.argv[1])
