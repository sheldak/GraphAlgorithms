import sys

from dimacs import loadWeightedGraph


def find(v_set, vertex):
    if vertex == v_set[vertex][0]:
        return vertex
    else:
        v_set[vertex][0] = find(v_set, v_set[vertex][0])
        return v_set[vertex][0]


def union(v_set, v1, v2):
    rep1 = find(v_set, v1)
    rep2 = find(v_set, v2)

    if v_set[rep1][1] >= v_set[rep2][1]:
        v_set[rep2][0] = rep1

        if v_set[rep1][1] == v_set[rep2][1]:
            v_set[rep1][1] += 1
    else:
        v_set[rep1][0] = rep2


def check_disjoint(v_set, v1, v2):
    return not v_set[find(v_set, v1)][0] == v_set[find(v_set, v2)][0]


def find_and_union(v, edge_list):
    v_set = [[i, 0] for i in range(v + 1)]  # [index, rank]

    edge_list.sort(key=lambda x: x[2], reverse=True)

    i = 0
    while i < len(edge_list) and check_disjoint(v_set, 1, 2):
        union(v_set, edge_list[i][0], edge_list[i][1])
        i += 1

    print(edge_list[i-1][2])


(v_len, edges) = loadWeightedGraph(sys.argv[1])  # reading graph
find_and_union(v_len, edges)
