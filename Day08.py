import time
import re
import itertools
from math import gcd

def calcLCM(list):
    lcm = 1
    for m in list:
        lcm = lcm * m // gcd(lcm, m)
    return lcm

def search(locations, cmd, guide):
    stepsRequired = [0]*len(locations)

    for round in itertools.count():
        for i, location in enumerate(locations):
            locations[i] = guide[location][cmd[(round) % len(cmd)]]
            if locations[i][2] == "Z" and stepsRequired[i] == 0 and (round+1) % len(cmd) == 0:
                stepsRequired[i] = round+1

        round += 1
        if (min(stepsRequired) > 0):
            break

    return calcLCM(stepsRequired)


def solve(part, filename):
    f = open(filename)
    lines = f.read().split("\n\n")

    cmd = list(map(int, [c for c in lines[0].strip().replace("L","0").replace("R","1")]))
    guide = {}

    for l in lines[1].split("\n"):
        m = re.search("^([A-Z0-9]{3})\s\=\s\(([A-Z0-9]{3})\,\s([A-Z0-9]{3})\)", l)
        if (m): guide[m.group(1)] = (m.group(2), m.group(3))

    if part == 1:
        result = search(["AAA"], cmd, guide)
    else:
        result = search([k for k in list(guide.keys()) if k[2] == "A"], cmd, guide)

    return result

start = time.time()
filename = "input/input08-sample.txt"
p1 = solve(1, filename)
print("Part 1 (Example): ", p1)

filename = "input/input08-sample2.txt"
p2 = solve(2, filename)
print('Part 2 (Example): ', p2)

filename = "input/input08.txt"
p1 = solve(1, filename)
print("Part 1 (Data): ", p1)
p2 = solve(2, filename)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
