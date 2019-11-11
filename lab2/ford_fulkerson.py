import sys
from dimacs import loadDirectedWeightedGraph
from queue import Queue


class Edge:
    def __init__(self, to, flow, capacity):
        self.to = to
        self.flow = flow
        self.capacity = capacity


def dfs(graph, graph_matrix, max_capacity, source, sink):
    visited = [False] * len(graph)
    parent = [0] * len(graph)
    max_flow = [0] * len(graph)

    stack = [source]
    max_flow[source] = max_capacity

    while len(stack) > 0 and not visited[sink]:
        curr_v = stack.pop()

        visited[curr_v] = True

        for i in range(len(graph[curr_v])):
            if not visited[graph[curr_v][i].to] and min(graph_matrix[curr_v][graph[curr_v][i].to], max_flow[curr_v]) > \
                    max_flow[graph[curr_v][i].to]:
                max_flow[graph[curr_v][i].to] = min(graph_matrix[curr_v][graph[curr_v][i].to], max_flow[curr_v])
                parent[graph[curr_v][i].to] = curr_v
                stack.append(graph[curr_v][i].to)

    if max_flow[sink] > 0:
        return parent, max_flow[sink]

    return None, None


def bfs(graph, graph_matrix, max_capacity, source, sink):
    visited = [False] * len(graph)
    parent = [0] * len(graph)
    max_flow = [0] * len(graph)

    max_flow[source] = max_capacity

    q = Queue()
    q.put(source)
    while not q.empty() and not visited[sink]:
        curr_v = q.get()

        visited[curr_v] = True
        for i in range(len(graph[curr_v])):
            if not visited[graph[curr_v][i].to] and min(graph_matrix[curr_v][graph[curr_v][i].to], max_flow[curr_v]) > \
                    max_flow[graph[curr_v][i].to]:
                max_flow[graph[curr_v][i].to] = min(graph_matrix[curr_v][graph[curr_v][i].to], max_flow[curr_v])
                parent[graph[curr_v][i].to] = curr_v
                q.put(graph[curr_v][i].to)

    if max_flow[sink] > 0:
        return parent, max_flow[sink]

    return None, None


def make_residual_graph(graph_matrix, path, flow, source, sink):
    curr_v = sink
    while curr_v != source:
        graph_matrix[curr_v][path[curr_v]] += flow
        graph_matrix[path[curr_v]][curr_v] -= flow
        curr_v = path[curr_v]


def ford_fulkerson(graph, graph_matrix, max_capacity, source, sink, search=bfs):
    path, flow = search(graph, graph_matrix, max_capacity, source, sink)
    max_flow = 0

    while path and flow:
        make_residual_graph(graph_matrix, path, flow, source, sink)
        max_flow += flow
        path, flow = bfs(graph, graph_matrix, max_capacity, source, sink)

    return max_flow


# (v_len, edges) = loadDirectedWeightedGraph(sys.argv[1])
#
# graph = [[] for v in range(v_len + 1)]  # for using in F-F
# graph_matrix = [[] for v in range(v_len + 1)]  # for checking capacity
#
# for i in range(1, v_len + 1):
#     for j in range(0, v_len + 1):
#         graph_matrix[i].append(0)
#
# max_capacity = 0
# for (x, y, c) in edges:
#     if c > max_capacity:
#         max_capacity = c
#
#     graph[x].append(Edge(y, 0, c))
#     graph[y].append(Edge(x, 0, 0))
#     graph_matrix[x][y] = c
#
# print(ford_fulkerson(graph, graph_matrix, max_capacity, 1, len(graph)-1))
