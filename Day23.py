import time
from collections import defaultdict
from collections import deque

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def def_value_dict():
    return {}


def def_value():
    return "."


def part1(grid, width, height, pos, visited):
    target = (width - 2, height - 1)
    if pos != (1, 0):
        visited[pos] = True

    while True:
        queue = []
        for dx, dy in directions:
            nx = pos[0] + dx
            ny = pos[1] + dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[nx][ny] in [".", ">", "<", "^", "v"]:
                    if (nx, ny) not in visited:
                        ok = True
                        match (grid[nx][ny]):
                            case ">":
                                if dx != 1: ok = False
                            case "<":
                                if dx != -1: ok = False
                            case "^":
                                if dy != -1: ok = False
                            case "v":
                                if dy != 1: ok = False
                        if ok:
                            queue.append((nx, ny))

        if len(queue) == 1:
            # just continue without recursion
            visited[queue[0]] = True
            if queue[0] == target:
                return len(visited)
            else:
                pos = queue[0]
        elif len(queue) > 0:
            # recursion
            return max([part1(grid, width, height, n, dict(visited)) for n in queue])
        else:
            return -1


def shortestPath(grid, vertices, width, height, a, b):
    target = b
    visited = {}
    queue = deque()
    queue.append((a, 0))
    distance = -1
    while queue:
        pos, distance = queue.popleft()

        if pos == target:
            return distance

        for dx, dy in directions:
            nx = pos[0] + dx
            ny = pos[1] + dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[nx][ny] != "#" and ((nx, ny) not in vertices or (nx, ny) == target):
                    if (nx, ny) not in visited:
                        visited[(nx, ny)] = True
                        queue.append(((nx, ny), distance + 1))

    return -1


def findVertices(grid, width, height):
    vertices = {(1, 0)}
    vertices.add((width - 2, height - 1))
    for y in range(height):
        for x in range(width):
            if grid[x][y] in [".", "<", ">", "^", "v"]:
                options = 0
                for dx, dy in directions:
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if grid[nx][ny] != "#":
                            options += 1
                if options > 2:
                    vertices.add((x, y))
    return vertices


def constructGraph(grid, vertices, width, height):
    graph = defaultdict(def_value_dict)
    for a in vertices:
        for b in vertices:
            if b < a:
                dist = shortestPath(grid, vertices, width, height, a, b)
                if dist > 0:
                    graph[a][b] = dist
                    graph[b][a] = dist
    return graph



def part2(graph, start, target, length, visited):
    result = -1
    if start == target:
        return length

    else:
        visited.add(start)

        for neighbour in graph[start]:
            if neighbour not in visited:
                result = max(result, part2(graph, neighbour, target, length + graph[start][neighbour], visited))

        visited.remove(start)
        return result


def solve(filename):
    f = open(filename)

    rows = f.read().strip().split("\n")
    grid = list(map(list, zip(*rows)))

    width = len(grid[0])
    height = len(grid)

    result1 = part1(grid, width, height, (1, 0), {})
    result2 = part2(constructGraph(grid, findVertices(grid, width, height), width, height), (1, 0), (width - 2, height - 1), 0, set())

    return result1, result2


start = time.time()
filename = "input/input23-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input23.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)
print("Total time: ", time.time() - start)
