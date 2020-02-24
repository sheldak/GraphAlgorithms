import sys

from lexBFSAndPEO import lex_bfs, load_graph


def max_clique(graph):
    lex_list = lex_bfs(graph)

    max_clique_size = 0

    for i in range(len(lex_list)):
        curr_clique_size = 0
        for neigh_index in range(i):
            if lex_list[neigh_index] in graph[lex_list[i]].out:
                curr_clique_size += 1

        if curr_clique_size + 1 > max_clique_size:
            max_clique_size = curr_clique_size + 1

    return max_clique_size


def find_max_clique(file_path):
    graph = load_graph(file_path)

    print(max_clique(graph))


# find_max_clique("maxclique/AT")
find_max_clique(sys.argv[1])
