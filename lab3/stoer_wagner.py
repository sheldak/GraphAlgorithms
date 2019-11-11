import sys
from queue import PriorityQueue

from dimacs import *


class Vertex:
    def __init__(self, i):
        self.edges = {}  # słownik par mapujący wierzchołki do których są krawędzie na ich wagi
        self.vertices = [i]
        self.deactivated = False

    def add_edge(self, to, weight):
        self.edges[to] = self.edges.get(to, 0) + weight  # dodaj krawędź do zadanego wierzchołka
        # o zadanej wadze; a jeśli taka krawędź
        # istnieje, to dodaj do niej wagę

    def del_edge(self, to):
        del self.edges[to]  # usuń krawędź do zadanego wierzchołka


def print_graph(G):
    for v in range(1, len(G)):
        print("Vertex: " + str(G[v].vertices) + ", edges: ", end='')
        for e in G[v].edges:
            print(str(e) + ": " + str(G[v].edges[e]) + ";  ", end='')

        if G[v].deactivated:
            print("deactivated", end='')

        print("")
    print("")


def merge_vertices(G, x, y):
    for z in G[y].edges:
        G[x].add_edge(z, G[y].edges[z])
        G[z].add_edge(x, G[y].edges[z])

    for z in list(G[y].edges.keys()):
        G[y].del_edge(z)
        G[z].del_edge(y)

    if x in G[x].edges:
        G[x].del_edge(x)

    G[x].vertices.append(y)
    G[y].deactivated = True


def minimum_cut_phase(G, curr_size):
    start = 1
    S = [start]

    weight_sum = [0 for i in range(len(G))]
    queue = PriorityQueue()

    for v in G[start].edges:
        queue.put((-1 * G[start].edges[v], v))
        weight_sum[start] += G[start].edges[v]

    s = 1
    t = 0
    while len(S) < curr_size:
        v = queue.get()

        if weight_sum[v[1]] == 0:
            for u in G[v[1]].edges:
                new_weight = -1 * v[0] + G[v[1]].edges[u]
                queue.put((-1 * new_weight, u))
                weight_sum[v[1]] += G[v[1]].edges[u]

            S.append(v[1])
            t = s
            s = v[1]
            print(S, s, t)

    merge_vertices(G, s, t)
    print(weight_sum[s])
    return weight_sum[s]


def stoer_wagner(G):
    result = len(G)-1   # maximum possible edge connectivity
    curr_size = len(G)-1

    while curr_size > 1:
        print_graph(G)
        result = min(minimum_cut_phase(G, curr_size), result)
        curr_size -= 1

    return result


(v_len, edges) = loadWeightedGraph("examples/geo20_2c")        # reading graph

G = [Vertex(i) for i in range(v_len+1)]

for (x, y, c) in edges:
    G[x].add_edge(y, c)
    G[y].add_edge(x, c)

print(stoer_wagner(G))

# print_graph(G)
