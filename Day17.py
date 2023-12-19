import time
import math
import heapq


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = math.inf
        self.predecessor = (-1, -1)
        self.stepCount = 0
        self.direction = (0, 0)

    def __lt__(self, other):
        return self.value < other.value

    def __lte__(self, other):
        return self.value <= other.value


def calc(grid, target, minStep, maxStep):
    start = Node(0, 0)
    start.value = 0

    width = target[0]
    height = target[1]

    q = [start]
    visited = {}

    while q:
        current = heapq.heappop(q)
        if current.x == target[0] and current.y == target[1]:
            # trace back / print path
            p = current
            if p.stepCount < minStep:
                continue

            if False:  # printing for debug purposed only
                path = {}
                while (p.x, p.y) != (0, 0):
                    path[(p.x, p.y)] = p
                    p = p.predecessor

                for y in range(height + 1):
                    for x in range(width + 1):
                        if (x, y) in path:
                            node = path[(x, y)]
                            direction = node.direction
                            match direction:
                                case (1, 0):
                                    c = ">"
                                case (-1, 0):
                                    c = "<"
                                case (0, 1):
                                    c = "v"
                                case (0, -1):
                                    c = "^"

                            print(c, end="")
                        else:
                            print(grid[(x, y)], end="")
                    print()
            return current.value
        else:
            if current.direction != (0, 0):
                if current.stepCount < maxStep:
                    dirSet = [current.direction]
                else:
                    dirSet = []

            else:
                dirSet = [(1, 0), (0, 1)]

            if current.stepCount >= minStep:
                match current.direction:
                    case (0, 0):
                        dirSet.append((1, 0))
                        dirSet.append((0, 1))
                    case (1, 0):
                        dirSet.append((0, 1))
                        dirSet.append((0, -1))
                    case (-1, 0):
                        dirSet.append((0, 1))
                        dirSet.append((0, -1))
                    case (0, 1):
                        dirSet.append((1, 0))
                        dirSet.append((-1, 0))
                    case (0, -1):
                        dirSet.append((1, 0))
                        dirSet.append((-1, 0))

            for (xDir, yDir) in dirSet:
                newPos = (current.x + xDir, current.y + yDir)

                if newPos[0] < 0 or newPos[0] > width or newPos[1] < 0 or newPos[1] > height:
                    continue

                if (xDir, yDir) == current.direction:
                    stepCount = current.stepCount + 1
                else:
                    stepCount = 1

                if (newPos, (xDir, yDir), stepCount) in visited:
                    node = visited[(newPos, (xDir, yDir), stepCount)]
                    if current.value + grid[newPos] < node.value:
                        node.value = current.value + grid[newPos]
                        node.predecessor = current
                        visited[(newPos, (xDir, yDir), stepCount)] = node
                else:
                    node = Node(newPos[0], newPos[1])
                    node.value = current.value + grid[newPos]
                    node.predecessor = current
                    node.direction = (xDir, yDir)
                    node.stepCount = stepCount
                    heapq.heappush(q, node)
                    visited[(newPos, (xDir, yDir), stepCount)] = node


def solve(filename):
    f = open(filename)

    grid = {}

    for height, r in enumerate(f.readlines()):
        for width, c in enumerate(r.strip()):
            grid[(width, height)] = int(c)

    grid[(0, 0)] = 0
    target = (width, height)

    result1 = calc(grid, target, 0, 3)
    result2 = calc(grid, target, 4, 10)

    return result1, result2


start = time.time()
filename = "input/input17-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input17-sample2.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input17.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
