import sys
import networkx as nx
from networkx.algorithms.planarity import check_planarity

from dimacs import loadWeightedGraph


def check_graph_planarity(path):
    (v_num, edges) = loadWeightedGraph(path)

    graph = nx.Graph()

    nodes = [i for i in range(1, v_num+1)]
    graph.add_nodes_from(nodes)

    graph.add_weighted_edges_from(edges)

    print(1) if check_planarity(graph)[0] else print(0)


# check_graph_planarity("plnar/AT")
check_graph_planarity(sys.argv[1])
