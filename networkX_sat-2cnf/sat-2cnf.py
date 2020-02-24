import sys
import networkx as nx
from networkx.algorithms.components import strongly_connected_components
from networkx.algorithms.dag import topological_sort

from dimacs import loadCNFFormula


def get_scc(path):
    (v_len, edges) = loadCNFFormula(path)

    implication_graph = nx.DiGraph()

    nodes = [i for i in range(1, v_len + 1)] + [-i for i in range(1, v_len + 1)]
    implication_graph.add_nodes_from(nodes)

    for x, y in edges:
        implication_graph.add_edge(-x, y)
        implication_graph.add_edge(-y, x)

    scc_gen = strongly_connected_components(implication_graph)
    scc = {}

    i = 0
    for s in scc_gen:
        new_set = set()
        for node in s:
            new_set.add(node)

        scc[i] = new_set
        i += 1

    return scc, implication_graph


def sat_2cnf_satisfied(path, scc=None):
    if not scc:
        scc, _ = get_scc(path)

    for s in scc.values():
        for node in s:
            if -node in s:
                return False

    return True


def test_if_satisfies(path):
    if sat_2cnf_satisfied(path):
        print(1)
    else:
        print(0)


def check_valuating(valuating, path):
    (v_len, edges) = loadCNFFormula(path)

    for node in range(1, v_len + 1):
        if valuating[node] == valuating[-node]:
            return False

    for u, v in edges:
        if not (valuating[u] or valuating[v]):
            return False

    return True


def sat_2cnf_valuating(path):
    scc, implication_graph = get_scc(path)

    if sat_2cnf_satisfied(path, scc):
        scc_graph = nx.DiGraph()

        nodes_scc = {}  # to have faster access to node's strongly connected component
        nodes_valuating = {}

        for s in scc.keys():
            scc_graph.add_node(s)

            for node in scc[s]:
                nodes_scc[node] = s
                nodes_valuating[node] = False

        for index, node_set in scc.items():
            for node in node_set:
                for neigh in implication_graph.adj[node]:
                    if index != nodes_scc[neigh]:
                        scc_graph.add_edge(index, nodes_scc[neigh])

        top_sort = topological_sort(scc_graph)

        for s in top_sort:
            for node in scc[s]:
                if not nodes_valuating[node]:
                    nodes_valuating[-node] = True

        print(1) if check_valuating(nodes_valuating, path) else print(0)
        print(nodes_valuating)


# test_if_satisfies("sat/sat5_10")
# test_if_satisfies(sys.argv[1])

sat_2cnf_valuating("sat/sat5_10")
