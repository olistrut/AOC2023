import time
from collections import defaultdict


def def_value():
    return 0

def simulate(grid, beam):
    height = len(grid)
    width = len(grid[0])
    visited = defaultdict(def_value)
    energized = [["."] * height for i in range(width)]

    queue = [beam]
    while queue:
        (x, y, xDir, yDir) = queue.pop(0)
        x = x+xDir
        y = y+yDir
        #print("Position: ", x,y, " - Direction: ", xDir, yDir)
        if not (0<=x<width and 0<=y<height):
            continue
        if (x, y, xDir, yDir) not in visited:
            visited[(x, y, xDir, yDir)] += 1
            # to trace path for debugging
            # if grid[x][y] == ".":
            #     match (xDir, yDir):
            #         case ( 1, 0):
            #             if energized[x][y] == ".":
            #                 energized[x][y] = ">"
            #             else:
            #                 energized[x][y] = "X"
            #         case (-1, 0):
            #             if energized[x][y] == ".":
            #                 energized[x][y] = "<"
            #             else:
            #                 energized[x][y] = "X"
            #         case ( 0, 1):
            #             if energized[x][y] == ".":
            #                 energized[x][y] = "v"
            #             else:
            #                 energized[x][y] = "X"
            #         case ( 0,-1):
            #             if energized[x][y] == ".":
            #                 energized[x][y] = "^"
            #             else:
            #                 energized[x][y] = "X"
            # else:
            #     energized[x][y] = grid[x][y]

            # set next steps
            #print("  Meeting with ",grid[x][y] ,"at position", x, y)

            match (grid[x][y], xDir, yDir):
                case(".", xDir, yDir):
                    queue.append((x, y, xDir, yDir))
                case("|", xDir, 0):
                    queue.append((x, y , 0,1))
                    queue.append((x, y, 0,-1))
                case("|", 0, yDir):
                    queue.append((x , y, xDir, yDir))
                case("-", 0, yDir):
                    queue.append((x ,y , +1,0 ))
                    queue.append((x , y , -1,0))
                case("-", xDir, 0):
                   queue.append((x  , y, xDir, yDir))
                case("/", xDir, yDir):
                    queue.append((x , y  , -yDir, -xDir))
                case("\\", xDir, yDir):
                    queue.append((x , y  , yDir, xDir))

    energized = {(x, y) for (x, y, _, _) in visited}
    return len(energized)

def solve(filename):

    result1 = result2 = 0
    f = open(filename)
    rows = f.read().strip().split("\n")
    grid = list(map(list, zip(*rows)))
    width = len(grid[0])
    height = len(grid)

    result1 = simulate(grid, (-1, 0, 1, 0))

    beams = []
    for y in range(height):
        beams.append((-1,y, 1,0))
        beams.append((width,y, -1,0))
    for x in range(width):
        beams.append((x,0, 0,1))
        beams.append((x,height, 0,-1))

    result2 = max([simulate(grid, b) for b in beams])

    return result1, result2



start = time.time()
filename = "input/input16-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

# 6565 is too low
filename = "input/input16.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
