import sys

from dimacs import loadWeightedGraph


def left(par):
    return par*2


def right(par):
    return par*2 + 1


def parent(child):
    return child//2


class MaxHeap:
    def __init__(self):
        self._queue = [0]
        self._size = 0

    def heapify(self, index):
        left_v = left(index)
        right_v = right(index)

        # checking if any child has higher flow value
        max_f_index = index
        if left_v <= self._size and self._queue[left_v][1] > self._queue[max_f_index][1]:
            max_f_index = left_v

        if right_v <= self._size and self._queue[right_v][1] > self._queue[max_f_index][1]:
            max_f_index = right_v

        if max_f_index != index:
            tmp = self._queue[max_f_index]
            self._queue[max_f_index] = self._queue[index]
            self._queue[index] = tmp
            self.heapify(max_f_index)

    def put(self,  vertex):
        self._queue.append(vertex)
        self._size += 1

        i = self._size
        while i > 1 and self._queue[i][1] > self._queue[parent(i)][1]:
            tmp = self._queue[i]
            self._queue[i] = self._queue[parent(i)]
            self._queue[parent(i)] = tmp

            i = parent(i)

    def pop(self):
        if self._size >= 1:
            vertex = self._queue[1]

            self._queue[1] = self._queue[self._size]
            self._queue.pop(self._size)

            self._size -= 1
            self.heapify(1)

            return vertex
        return [0, 0]  # returning whatever, no possibility to reach this code (I hope)

    def size(self):
        return self._size


def dijkstra(v, edge_list):
    graph = [[] for i in range(v + 1)]
    for (x, y, w) in edge_list:
        graph[x].append([y, w])
        graph[y].append([x, w])

    queue = MaxHeap()
    visited = [False] * (v+1)
    flow = [0] * (v+1)  # max flow to that vertex

    visited[1] = True
    for edge in graph[1]:
        queue.put(edge)
        flow[edge[0]] = edge[1]

    while queue.size() >= 1 and not visited[2]:
        max_v = queue.pop()
        visited[max_v[0]] = True

        for edge in graph[max_v[0]]:
            if flow[edge[0]] < edge[1] and flow[edge[0]] < flow[max_v[0]]:
                flow[edge[0]] = min(flow[max_v[0]], edge[1])
                queue.put(edge)

    print(flow[2])


(v_len, edges) = loadWeightedGraph(sys.argv[1])  # reading graph
dijkstra(v_len, edges)
