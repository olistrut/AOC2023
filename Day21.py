import time
from collections import defaultdict

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def def_value():
    return "."


def part1(grid, width, height, start, steps):
    queue = [(start, 0)]
    visited = {}

    while queue:
        (x, y), step = queue.pop(0)
        if (x, y) in visited:
            continue

        visited[(x, y)] = step

        for dx, dy in directions:
            newX = x + dx
            newY = y + dy
            if 0 <= newX < width and 0 <= newY < height and step < steps and grid[newX][newY] != '#':
                queue.append(((newX, newY), step + 1))

    # only return fields that were visited in an even step
    result1 = sum([1 for pos, v in visited.items() if v % 2 == 0])

    # for y in range(width):
    #    for x in range(height):
    #        if (x,y) in visited and visited[(x,y)] % 2 == 0 :
    #            print("O", end="")
    #        else:
    #            print(grid[x][y], end="")
    #    print()

    return result1


def runStepsPart2(listgrid, width, height, start, steps):
    grid = defaultdict(def_value)

    for x in range(width):
        for y in range(height):
            if listgrid[x][y] == '#':
                grid[(x, y)] = listgrid[x][y]

    queue = []
    queue.append((start, 0))
    visited = {}

    while queue:
        (x, y), step = queue.pop(0)
        if (x, y) in visited:
            continue

        visited[(x, y)] = step

        for dx, dy in directions:
            newX = x + dx
            newY = y + dy
            if step < steps and grid[(newX % width, newY % height)] != '#':
                queue.append(((newX, newY), step + 1))

    if steps % 2 == 0:
        return sum([1 for pos, v in visited.items() if v % 2 == 0])
    else:
        return sum([1 for pos, v in visited.items() if v % 2 == 1])


def part2(listgrid, width, height, start, target):
    base = target % width

    results = []
    diff = []
    diffofdiff = []

    for i, round in enumerate(range(base, base + 8 * width, width)):  # round should be 196 when we exit
        results.append(runStepsPart2(listgrid, width, height, start, round))
        if len(results) >= 2:
            diff.append(results[-1] - results[-2])
        if len(diff) >= 2:
            diffofdiff.append(diff[-1] - diff[-2])

        if len(diffofdiff) >= 3:
            if diffofdiff[-1] == diffofdiff[-2] == diffofdiff[-3]:
                break

    result = results[-1]  # 34125
    distance = diff[-1]  # 30290
    diffofdiff = diffofdiff[-1]  # 30188

    for i in range((target - round) // width):
        distance += diffofdiff
        result = result + distance
        round += width

    return result


def solve(filename, steps, target):
    f = open(filename)

    rows = f.read().strip().split("\n")
    grid = list(map(list, zip(*rows)))

    width = len(grid[0])
    height = len(grid)

    stones = 0
    for x in range(width):
        for y in range(height):
            if grid[x][y] == 'S':
                grid[x][y] = "."
                start = (x, y)
            elif grid[x][y] == '#':
                stones += 1

    result1 = part1(grid, width, height, start, steps)
    result2 = part2(grid, width, height, start, target)

    return result1, result2


start = time.time()

filename = "input/input21-sample.txt"
p1, p2 = solve(filename, 6, 1000)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input21.txt"
p1, p2 = solve(filename, 64, 26501365)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
