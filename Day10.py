import time
from collections import defaultdict


def def_value():
    return "."

steps = {"7": [ (-1,0), (0,1) ],  "J": [ (-1,0), (0,-1) ], "L": [ (1,0), (0,-1) ], "F": [ (1,0), (0,1) ], "-": [ (1,0), (-1,0)], "|": [ (0,-1), (0,1) ] }

vertical = set(("J","7","L","F","|"))

def solve(part, filename):

    f = open(filename)
    lines = f.read().strip().split("\n")

    field = defaultdict(def_value)

    pos = (0, 0)
    for y, l in enumerate(lines):
        height = y
        for x, c in enumerate(l):
            width = x
            field[(x, y)] = c
            if c == "S": pos = (x, y)
    height += 1
    width += 1

    # replace start character with appropriate pipe
    startDirections = set()
    if field[pos[0], pos[1]+1] in ["L", "J", "|"]: startDirections.add("down")
    if field[pos[0], pos[1]-1] in ["F", "7", "|"]: startDirections.add("up")
    if field[pos[0]-1, pos[1]] in ["F", "-", "L"]: startDirections.add("left")
    if field[pos[0]+1, pos[1]] in ["7", "-", "J"]: startDirections.add("right")

    if startDirections == {"down", "right"}: field[pos] = "F"
    elif startDirections == {"down", "left"}: field[pos] = "7"
    elif startDirections == {"up", "left"}: field[pos] = "J"
    elif startDirections == {"up", "right"}: field[pos] = "L"
    elif startDirections == {"down", "up"}: field[pos] = "|"
    elif startDirections == {"left", "right"}: field[pos] = ""

    distance = 1

    visited = {pos: True}

    while (pos != None):
        next = None
        for step in steps[field[pos]]:
            if (pos[0] + step[0], pos[1] + step[1]) not in visited:
                next = (pos[0] + step[0], pos[1] + step[1])
        pos = next
        visited[pos] = True
        distance += 1

    result1 = distance // 2

    for y in range(height+1):
        inside = False
        lastVertical = ""
        for x in range(width+1):
            c = field[(x,y)]
            if (x,y) in visited:
                if field[(x,y)] in vertical:
                    if not ((lastVertical == "L" and field[(x,y)] == "7") or (lastVertical == "F" and field[(x,y)] == "J")):
                        inside ^= True
                    lastVertical = field[(x,y)]
            elif inside == True:
                field[(x,y)] = "X"

    result2 = len([x for x in field.values() if x == "X"])

    # for y in range(height+1):
    #     for x in range(width+1):
    #         if (x,y) in visited:
    #             print(field[(x,y)], end="")
    #
    #         else:
    #             if field[(x,y)] == "X":
    #                 print("X", end="")
    #             else:
    #                 print(".", end="")
    #     print()

    return result1, result2

start = time.time()
filename = "input/input10-sample.txt"
p1, p2 = solve(1, filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input10-sample2.txt"
p1, p2 = solve(1, filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input10-sample3.txt"
p1, p2 = solve(1, filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input10-sample4.txt"
p1, p2 = solve(1, filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input10-sample5.txt"
p1, p2 = solve(1, filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input10.txt"
p1, p2 = solve(1, filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
