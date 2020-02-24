import sys

from lexBFSAndPEO import lex_bfs, load_graph


class Vertex:
    def __init__(self):
        self.children = []
        self.parent = 0


class Node:
    def __init__(self, vertex, time):
        self.vertices = [vertex]
        self.clique = set()

        self.parent = None
        self.children = []

        self.made_time = time

        self.disabled = False  # about edge between this node and its parent


def make_tree_preorder(tree, curr_node, tree_list):
    tree_list.append(curr_node)
    for child in tree[curr_node].children:
        make_tree_preorder(tree, child, tree_list)


def list_and_set_equal(a_list, a_set):
    for i in a_list:
        if i not in a_set:
            return False

    if len(a_list) == len(a_set):
        return True

    return False


def build_clique_tree(graph, lex_list):
    rn = [[] for _ in range(len(lex_list) + 1)]  # list of neighbours which precede vertex in lex_list

    for i in range(len(lex_list)):
        for neigh_index in range(i):
            if lex_list[neigh_index] in graph[lex_list[i]].out:
                rn[lex_list[i]].append(lex_list[neigh_index])

    vertices_tree = [Vertex() for _ in range(len(lex_list) + 1)]  # tree of vertices, index is a number of vertex

    # print(rn)

    for index in range(len(lex_list)):
        if rn[lex_list[index]]:
            vertices_tree[rn[lex_list[index]][-1]].children.append(lex_list[index])
            vertices_tree[lex_list[index]].parent = rn[lex_list[index]][-1]

    # for i in vertices_tree:
    #     print(i.parent)

    tree_preorder = []  # list with all vertices made by traversing vertices_tree preorder
    make_tree_preorder(vertices_tree, 1, tree_preorder)
    # print(tree_preorder)

    matched_clique = [Node(0, 0) for _ in range(len(lex_list) + 1)]  # every vertex has one clique matched with it

    time = 0  # to know the order of building cliques

    curr_node = Node(tree_preorder[0], time)  # making clique tree
    curr_node.clique.add(tree_preorder[0])
    matched_clique[tree_preorder[0]] = curr_node

    for index in range(1, len(tree_preorder)):
        time += 1

        while not vertices_tree[tree_preorder[index]].parent in curr_node.vertices:  # finding parent
            curr_node = curr_node.parent

        if list_and_set_equal(rn[tree_preorder[index]], curr_node.clique):    # adding vertex to current node
            curr_node.clique.add(tree_preorder[index])
            curr_node.vertices.append(tree_preorder[index])

            curr_node.made_time = time
        else:                                               # creating new node
            new_node = Node(tree_preorder[index], time)
            new_node.parent = curr_node
            curr_node.children.append(new_node)

            for vertex in rn[tree_preorder[index]]:
                new_node.clique.add(vertex)

            new_node.clique.add(tree_preorder[index])

            curr_node = new_node

        matched_clique[tree_preorder[index]] = curr_node

    # print(curr_node.parent.clique)
    # print(curr_node.parent.vertices)
    while curr_node.parent:
        curr_node = curr_node.parent

    # print("#######")
    # print(curr_node.clique)
    # for child in curr_node.children:
    #     print(child.clique)

    return curr_node, matched_clique


def find_last_clique_in_set(clique_set):
    last_clique = None

    for clique in clique_set:
        if not last_clique or clique.made_time > last_clique.made_time:
            last_clique = clique

    return last_clique


def add_all_cliques(clique_set, curr_clique):
    clique_set.add(curr_clique)

    for child in curr_clique.children:
        add_all_cliques(clique_set, child)


def get_cliques_with_pivot(clique_class, curr_clique, pivot):
    if pivot in curr_clique.clique:
        clique_class.add(curr_clique)

        for child in curr_clique.children:
            get_cliques_with_pivot(clique_class, child, pivot)


def find_classes_intersecting(intersected_clique_class, clique_classes_list):
    start = clique_classes_list[-1]
    for clique_class in clique_classes_list:
        if clique_class & intersected_clique_class:
            start = clique_class
            break

    end = clique_classes_list[-1]
    for index in range(clique_classes_list.index(start), len(clique_classes_list)):
        clique_class = clique_classes_list[index]
        if not clique_class & intersected_clique_class:
            end = clique_classes_list[index - 1]
            break

    return start, end


def build_clique_chain(clique_root, matched_clique):
    pivots = set()
    clique_classes_list = []

    # first set which will be in clique list
    first_class = set()  # all cliques

    add_all_cliques(first_class, clique_root)

    clique_classes_list.append(first_class)

    just_singletons = False
    while not just_singletons:
        just_singletons = True

        for index in range(len(clique_classes_list)):  # looking for a class with more than 1 clique
            clique_class = clique_classes_list[index]
            if len(clique_class) > 1:
                curr_clique_class = set()

                if not pivots:
                    last_clique = find_last_clique_in_set(clique_class)
                    clique_class.remove(last_clique)

                    curr_clique_class.add(last_clique)

                    clique_classes_list.insert(index+1, curr_clique_class)
                else:
                    pivot = pivots.pop()
                    get_cliques_with_pivot(curr_clique_class, matched_clique[pivot], pivot)

                    # all classes intersecting curr_clique_class
                    # are between start_class and end_class in clique_classes_list
                    start_class, end_class = find_classes_intersecting(curr_clique_class, clique_classes_list)

                    start_class_index = clique_classes_list.index(start_class)
                    clique_classes_list.remove(start_class)
                    sets_difference = start_class - curr_clique_class
                    sets_intersection = start_class & curr_clique_class

                    if sets_difference:
                        clique_classes_list.insert(start_class_index, sets_difference)
                        if sets_intersection:
                            clique_classes_list.insert(start_class_index + 1, sets_intersection)
                    elif sets_intersection:
                        clique_classes_list.insert(start_class_index, sets_intersection)

                    end_class_index = clique_classes_list.index(end_class)
                    clique_classes_list.remove(end_class)
                    sets_difference = end_class - curr_clique_class
                    sets_intersection = end_class & curr_clique_class

                    if sets_intersection:
                        clique_classes_list.insert(end_class_index, sets_intersection)
                        if sets_difference:
                            clique_classes_list.insert(end_class_index + 1, sets_difference)
                    elif sets_difference:
                        clique_classes_list.insert(end_class_index, sets_difference)

                for clique in curr_clique_class:
                    for child in clique.children:
                        if not child.disabled and child not in curr_clique_class:
                            pivots = pivots | clique.clique.intersection(child.clique)
                            child.disabled = True

                    if clique.parent and not clique.disabled and clique not in clique.parent.clique:
                        pivots = pivots | clique.clique.intersection(clique.parent.clique)
                        clique.disabled = True

                just_singletons = False
                break

    return clique_classes_list


def check_if_clique_chain(chain, graph_size):
    sequence_finished = [False for i in range(graph_size)]  # if sequence of cliques containing vertex i has ended
    in_curr_clique = set()  # list of vertices in curr clique
    # for i in range(graph_size - 1):
    for clique_class in chain:
        clique_as_set = clique_class.pop().clique

        new_vertices_set = set()

        for vertex in clique_as_set:
            if sequence_finished[vertex]:
                return False
            else:
                new_vertices_set.add(vertex)

        for vertex in in_curr_clique:
            if vertex not in clique_as_set:
                sequence_finished[vertex] = True

        in_curr_clique = new_vertices_set

    return True


def check_if_interval(file_path):
    graph = load_graph(file_path)

    lex_list = lex_bfs(graph)
    # print(lex_list)

    clique_root, matched_clique = build_clique_tree(graph, lex_list)

    potential_clique_chain = build_clique_chain(clique_root, matched_clique)

    print(1) if check_if_clique_chain(potential_clique_chain, len(lex_list) + 1) else print(0)

# check_if_interval("interval/interval-rnd10")
check_if_interval("interval-rnd10")
# check_if_interval(sys.argv[1])
