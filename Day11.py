import time

def calc(lines, offset):
    offsetListY = []
    offsetListX = []

    offsetCount = 0
    for i, line in enumerate(lines):
        if "#" not in line:
            offsetCount += 1
        offsetListY.append(offset * offsetCount)

    for x in range(len(lines[0])):
        if "#" not in [line[x] for line in lines]:
            offsetCount += 1
        offsetListX.append(offset * offsetCount)

    galaxies = []

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if line[x] == "#":
                galaxies.append((x+offsetListX[x], y+offsetListY[y]))

    result = 0
    for i in range(len(galaxies)):
        for j in range(i, len(galaxies)):
            g1 = galaxies[i]
            g2 = galaxies[j]
            result += abs(g2[0] - g1[0]) + abs(g2[1] - g1[1])

    return result


def solve(filename):
    f = open(filename)
    lines = f.read().strip().split("\n")
    return calc(lines, 1), calc(lines, 999999)


start = time.time()
filename = "input/input11-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input11.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
