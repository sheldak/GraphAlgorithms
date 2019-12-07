import sys

from lexBFSAndPEO import lex_bfs, load_graph


def coloring(graph):
    lex_list = lex_bfs(graph)

    colors = []
    max_color = 0

    for index in range(len(lex_list)):
        used_colors = set()
        for prev_index in range(index):
            if lex_list[index] in graph[lex_list[prev_index]].out:
                used_colors.add(colors[prev_index])

        curr_color = 1
        while curr_color in used_colors:
            curr_color += 1

        colors.append(curr_color)

        if curr_color > max_color:
            max_color = curr_color

    return max_color


def check_coloring(file_path):
    graph = load_graph(file_path)

    print(coloring(graph))


# check_coloring("coloring/house")
check_coloring(sys.argv[1])
