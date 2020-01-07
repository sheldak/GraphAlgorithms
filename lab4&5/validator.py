import sys
from time import time
import os
from statistics import mean, median
from subprocess import check_output

# python3 validator.py "/home/sheldak/dev/PyCharm/GraphAlgorithms/lab4&5/chordal/" "/home/sheldak/dev/PyCharm/GraphAlgorithms/lab4&5/lexBFSAndPEO.py"
# python3 validator.py "/home/sheldak/dev/PyCharm/GraphAlgorithms/lab4&5/maxclique/" "/home/sheldak/dev/PyCharm/GraphAlgorithms/lab4&5/maxClique.py"
# python3 validator.py "/home/sheldak/dev/PyCharm/GraphAlgorithms/lab4&5/coloring/" "/home/sheldak/dev/PyCharm/GraphAlgorithms/lab4&5/coloring.py"
# python3 validator.py "/home/sheldak/dev/PyCharm/GraphAlgorithms/lab4&5/interval/" "/home/sheldak/dev/PyCharm/GraphAlgorithms/lab4&5/interval.py"

solutions = ""
script = ""
expected = "0"

if len(sys.argv) < 3:
    print("Not enough args!")
    sys.exit()

if not os.path.isdir(sys.argv[1]):      # directory with examples of graphs
    print("The solutions path is incorrect!")
    sys.exit()
else:
    solutions = sys.argv[1]

if not os.path.isfile(sys.argv[2]):      # directory with algorithms
    print("The script path is incorrect!")
    sys.exit()
else:
    script = sys.argv[2]

if os.path.isfile(script) and script.endswith(".py"):

    print("Current algorithm:", script[:-3])
    stats = []      # to display mean and median after all tests for that algorithm

    for filename in os.listdir(solutions):
        path = solutions + filename
        fp = open(path)
        first_line = fp.readline()
        if first_line[0] == 'c':
            expected = ''.join(filter(str.isdigit, first_line))     # reading solution from the graph file
            start_time = time()
            output = check_output(["python3", script, path])   # reading algorithm's output
            end_time = time()
            response = int(output)
            expected = int(expected)
            if response == expected:    # checking if algorithm makes right output
                print("Accepted on: ", filename, " in time: ", end_time - start_time)
                stats.append(end_time-start_time)
            else:
                print("Failed on: ", filename)

        fp.close()

    print("mean: ", mean(stats), "  median: ", median(stats))   # printing stats
