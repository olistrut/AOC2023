import time
from collections import defaultdict

def def_value():
    return "."

def checkCoords(x, y, map, currentGears):
    if map[(x, y)] == "*": currentGears[(x,y)] = True
    return map[(x, y)] != '.' and map[(x, y)].isdigit() == False

def solve(filename):
    result1 = 0
    result2 = 0

    map = defaultdict(def_value)
    # Key: (x,y) coordinate of gear ("*"). Value: list of adjacent numbers (int)
    gears = defaultdict(list)

    f = open(filename)
    file = open(filename)

    y = x = 1

    while s := f.readline():
        x = 1
        for c in s.strip():
            map[(x,y)] = c
            x += 1
        y += 1

    height = y
    width = x

    number = ""
    hasAdjacent = False
    currentGears = {}

    neighbors = [(-1,0),(-1,-1),(-1,+1),(0,-1),(0,1),(1,-1),(1,1), (1,0)]

    for y in range(height):
        for x in range(width):
            c = map[(x,y)]
            if c.isdigit():
                number += c
                for neighbor in neighbors:
                    hasAdjacent |= checkCoords(x + neighbor[0], y + neighbor[1], map, currentGears)
            else:
                if number != "":
                    if hasAdjacent: result1 += int(number)

                    if len(currentGears) > 0:
                        for gear in currentGears.keys():
                            gears[gear].append(number)

                    hasAdjacent = False
                    currentGears = {}

                number = ''

    for n in gears.values():
        if len(n) == 2: result2 += int(n[0]) * int(n[1])

    return result1, result2


start = time.time()
filename = "input/input03-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input03.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)
print("Total time: ", time.time() - start)
