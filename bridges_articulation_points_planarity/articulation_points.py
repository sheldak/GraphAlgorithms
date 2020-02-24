from dimacs import loadWeightedGraph


class TTNode:
    def __init__(self, idx, parent):
        self.idx = idx            # indeks wierzcholka w kolejnosci DFS (nie jego nazwa w grafie!)
        self.parent = parent      # rodzic wierzcholka (nazwa)
        self.children = set()     # zbior nazw potomkow tego wierzcholka w drzewie DFS
        self.back = set()         # zbior nazw wierzcholkow, do ktorych prowadza krawedzie wsteczne
        self.out = []             # lista wierzchołków docelowych krawedzi wychodzacych w kolejnosci TT-prec


def dfs(graph):
    visited = [False for _ in range(len(graph)+1)]

    low = [len(graph) for _ in range(len(graph)+1)]

    tremaux_tree = [TTNode(0, None) for _ in range(len(graph)+1)]

    def dfs_visit(curr_node, curr_idx):
        # TODO curr_idx is changing just locally
        visited[curr_node] = True

        for neigh in graph[curr_node]:
            if visited[neigh]:
                tremaux_tree[curr_node].back.add(neigh)

        for neigh in graph[curr_node]:
            if not visited[neigh]:
                curr_idx += 1
                new_node = TTNode(curr_idx, tremaux_tree[curr_node])
                tremaux_tree[neigh] = new_node

                tremaux_tree[curr_node].children.add(neigh)
                dfs_visit(neigh, curr_idx)

        min_children = tremaux_tree[curr_node].idx
        for child in tremaux_tree[curr_node].children:
            min_children = min(min_children, low[child])

        min_back = tremaux_tree[curr_node].idx
        for back in tremaux_tree[curr_node].back:
            min_back = min(min_back, tremaux_tree[back].idx)

        low[curr_node] = min(tremaux_tree[curr_node].idx, min_children, min_back)

    start_node = TTNode(0, None)
    tremaux_tree[1] = start_node
    visited[1] = True

    dfs_visit(1, 0)

    return tremaux_tree, low


def articulation_points():
    v_len, edges = loadWeightedGraph("articulation/AT")

    graph = [[] for _ in range(v_len + 1)]

    for x, y, _ in edges:
        graph[x].append(y)
        graph[y].append(x)

    tremaux_tree, low = dfs(graph)

    print(tremaux_tree)
    for node in tremaux_tree:
        print(node.idx)
    print(low)


articulation_points()

