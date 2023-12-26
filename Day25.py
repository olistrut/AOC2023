import time
import networkx as nx
from random import randint
from networkx.algorithms import flow


def solve(filename):
    result1 = result2 = 0
    f = open(filename)
    G = nx.Graph()
    nodes = {}

    while s := f.readline():
        part, r = s.strip().split(": ")
        connected = r.split(" ")
        nodes[part] = True
        for c in connected:
            G.add_edge(part, c, capacity=1)
            nodes[c] = True

    result1 = len(nodes)-1
    while result1 == len(nodes)-1:
        # run minimum cut for 2 random elements. result only counts if it does not split graph into 1 node and len(nodes)-1 other nodes. otherwise try again.
        a = list(nodes.keys())[randint(0, len(nodes))]
        b = list(nodes.keys())[randint(0, len(nodes))]

        r = flow.minimum_cut(G, a, b)
        if len(r[1]) == 2:
            result1 = len(r[1][0]) *  len(r[1][1])

    return result1, result2


start = time.time()

filename = "input/input25-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input25.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
