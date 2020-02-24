import sys

from ford_fulkerson import Edge, ford_fulkerson
from dimacs import loadDirectedWeightedGraph


def make_graphs(v_len, edges):
    graph = [[] for v in range(v_len + 1)]  # for using in F-F
    graph_matrix = [[] for v in range(v_len + 1)]  # for checking capacity

    for i in range(1, v_len + 1):
        for j in range(0, v_len + 1):
            graph_matrix[i].append(1)

    for (x, y, c) in edges:
        graph[x].append(Edge(y, 0, 1))
        graph[y].append(Edge(x, 0, 1))

    return graph, graph_matrix


def edge_connectivity(v_len, edges):
    min_flow = v_len
    for i in range(2, v_len+1):
        graph, graph_matrix = make_graphs(v_len, edges)
        curr_flow = ford_fulkerson(graph, graph_matrix, 1, 1, i)
        min_flow = min(min_flow, curr_flow)

    return min_flow


(v_len, edges) = loadDirectedWeightedGraph(sys.argv[1])
#(v_len, edges) = loadDirectedWeightedGraph("connectivity/path")

print(edge_connectivity(v_len, edges))
