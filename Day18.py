import time
import math
from collections import defaultdict


def def_value():
    return "."


direction1 = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}
direction2 = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def calculate(filename):
    result = 0
    f = open(filename)
    grid = defaultdict(def_value)

    x = 0
    y = 0
    corners = [math.inf, math.inf, 0, 0]
    for s in f.readlines():
        dir, steps, color = s.strip().split(" ")

        steps = int(steps)
        vector = direction1[dir]

        for step in range(int(steps)):
            x = x + vector[0]
            y = y + vector[1]

            grid[(x, y)] = "#"
            if x <= corners[0]:
                corners[0] = x
            if x >= corners[2]:
                corners[2] = x
            if y <= corners[1]:
                corners[1] = y
            if y >= corners[3]:
                corners[3] = y

    for y in range(corners[1] - 1, corners[3] + 1):
        inside = False
        upperhalf = False
        lowerhalf = False
        for x in range(corners[0] - 1, corners[2] + 2):
            if not (x, y) in grid:
                if inside:
                    result += 1
                #    print("x", end="")
                # else:
                #   print(".", end="")
            else:
                # print("#", end="")
                if (x - 1, y) not in grid and (x + 1, y) not in grid:
                    # vertical edge
                    inside = not inside
                elif (x - 1, y) in grid and (x + 1, y) not in grid and ((x, y - 1) in grid or (x, y + 1) in grid):
                    # end corner:

                    if (x, y - 1) in grid:
                        upperhalf = True
                    else:
                        lowerhalf = True

                    if upperhalf and lowerhalf:
                        inside = not inside

                    upperhalf = False
                    lowerhalf = False

                elif (x - 1, y) not in grid and ((x, y - 1) in grid or (x, y + 1) in grid):
                    # begin corner
                    upperhalf = False
                    lowerhalf = False
                    if (x, y - 1) in grid:
                        upperhalf = True
                    else:
                        lowerhalf = True

                result += 1
        # print()

    return result


##############################
def calculate2(part, filename):
    f = open(filename)

    vertices = [(0, 0)]

    x = 0
    y = 0
    border = 0
    for s in f.readlines():
        dir, steps, color = s.strip().split(" ")

        if part == 1:
            steps = int(steps)
        else:
            steps = int("0x" + color[2:-2], 16)

        if part == 1:
            vector = direction1[dir]
        else:
            vector = direction2[int(color[-2])]

        x = x + vector[0] * steps
        y = y + vector[1] * steps

        vertices.append((x, y))
        border += steps

    shoelace = 0
    for i in range(len(vertices) - 1):
        v1 = vertices[i]
        v2 = vertices[i + 1]
        shoelace += v1[0] * v2[1] - v1[1] * v2[0]
    shoelace /= 2
    return int(abs(shoelace) + border // 2 + 1)


def solve(filename):
    result1 = calculate( filename)
    print("R1 old: ", result1)
    result1 = calculate2(1, filename)
    print("R1 new: ", result1)
    result2 = calculate2(2, filename)

    return result1, result2


start = time.time()

filename = "input/input18-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input18-sample2.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input18.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
