from multiprocessing import Queue
import sys

import dimacs


def make_adj_list(v, edge_list):    # creating adjacency list
    graph = [[] for i in range(v + 1)]
    for (x, y, w) in edge_list:
        graph[x].append([y, w])
        graph[y].append([x, w])

    return graph


def dfs(graph, weight):     # iterative version of dfs
    visited = [False] * len(graph)
    stack = [1]

    while len(stack) > 0:
        curr_v = stack.pop()
        if curr_v == 2:
            return True

        visited[curr_v] = True

        for i in range(len(graph[curr_v])):
            if not visited[graph[curr_v][i][0]] and graph[curr_v][i][1] >= weight:
                stack.append(graph[curr_v][i][0])

    return False


def dfs_rec(graph, weight):     # recursive version of dfs
    visited = [False] * len(graph)

    return dfs_visit(graph, 1, weight, visited)


def dfs_visit(graph, curr_v, weight, visited):
    visited[curr_v] = True
    if curr_v == 2:
        return True

    for i in range(len(graph[curr_v])):
        if not visited[graph[curr_v][i][0]] and graph[curr_v][i][1] >= weight:
            if dfs_visit(graph, graph[curr_v][i][0], weight, visited):
                return True

    return False


def bfs(graph, weight):
    visited = [False] * len(graph)
    q = Queue()

    q.put(1)

    while not q.empty():
        curr_v = q.get()
        if curr_v == 2:
            return True

        visited[curr_v] = True

        for i in range(len(graph[curr_v])):
            if not visited[graph[curr_v][i][0]] and graph[curr_v][i][1] >= weight:
                q.put(graph[curr_v][i][0])

    return False


def binary_search(v, edge_list, search_algorithm):  # search algorithm: dfs, dfs_rec or bfs
    graph = make_adj_list(v, edge_list)
    edge_list.sort(key=lambda l: l[2])

    max_weight = edge_list[len(edge_list)-1][2]
    min_weight = edge_list[0][2]

    curr_weight = (max_weight + min_weight) // 2
    while max_weight - min_weight > 1:
        if search_algorithm(graph, curr_weight):
            min_weight = curr_weight
        else:
            max_weight = curr_weight

        curr_weight = (max_weight+min_weight)//2

    if search_algorithm(graph, min_weight+1):
        print(min_weight+1)
    else:
        print(min_weight)


(v_len, edges) = dimacs.loadWeightedGraph(sys.argv[1])  # reading graph
binary_search(v_len, edges, dfs)
