import sys
import networkx as nx
from networkx.algorithms.flow import maximum_flow

from dimacs import loadWeightedGraph


def flow(path):
    (v_num, edges) = loadWeightedGraph(path)

    graph = nx.DiGraph()

    nodes = [i for i in range(1, v_num + 1)]
    graph.add_nodes_from(nodes)

    for (x, y, c) in edges:
        graph.add_edge(x, y)
        graph[x][y]['capacity'] = c

    print(maximum_flow(graph, 1, v_num)[0])


# flow("flow/simple")
flow(sys.argv[1])

