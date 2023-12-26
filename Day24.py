import time
from itertools import product, combinations

from sympy import symbols
import sympy


def part1(hailstones, lowerbound, upperbound):
    result = 0

    for path1, path2 in combinations(hailstones, 2):
        # y = ax + b
        # a = vy/vx
        a1 = path1[4] / path1[3]
        a2 = path2[4] / path2[3]
        # b = y/ax
        b1 = path1[1] - (a1 * path1[0])
        b2 = path2[1] - (a2 * path2[0])

        # x intersect =
        if (a2 - a1) != 0:
            x = (b2 - b1) / (a1 - a2)

            y1 = a1 * x + b1
            y2 = a2 * x + b2

            # print(path1, path2, "meeting at", x, y1, y2)

            if lowerbound < x < upperbound and lowerbound < y1 < upperbound:
                if not ((path1[3] > 0 and x < path1[0]) or (path2[3] > 0 and x < path2[0]) or (path1[3] <= 0 and x > path1[0]) or (path2[3] <= 0 and x > path2[0])):
                    result += 1

    return result


def part2bruteforce(hailstones):
    lowX = min([x[0] for x in hailstones])
    highX = max([x[0] for x in hailstones])
    lowY = min([y[1] for y in hailstones])
    highY = max([y[1] for y in hailstones])
    lowZ = min([z[2] for z in hailstones])
    highZ = max([z[2] for z in hailstones])

    minSpeedXPositive = sum([h[3] for h in hailstones if h[0] == highX])
    minSpeedXNegative = sum([h[3] for h in hailstones if h[0] == lowX])

    breaks = 0
    runs = 0
    xCandidates = {}
    # find x candidates
    for i in range(0, 1000):
        for k in [-1, +1]:
            for l in [-1, +1]:
                for j in range(0, 20):
                    px = (highX - lowX) // 2 + k * i
                    vx = l * j
                    runs += 1
                    if 0 < vx < minSpeedXPositive or (0 > vx > minSpeedXNegative):
                        breaks += 1
                        break
                    if vx > 0 and px >= highX or (vx < 0 and px <= lowX):
                        breaks += 1
                        break
                    for h in hailstones:
                        if vx - h[3] != 0:
                            t = (h[0] - px) / (vx - h[3])
                            if not t.is_integer() or t <= 0:
                                break
                        elif px != h[1]:
                            break

                    else:
                        xCandidates[(px, vx)] = True

    yCandidates = {}
    # find y candidates
    for i in range(0, 1000):
        for j in range(0, 50):
            for k in [-1, +1]:
                for l in [-1, +1]:
                    py = (highY - lowY) // 2 + k * i
                    vy = 10 + l * j

                    for h in hailstones:
                        if vy - h[4] != 0:
                            t = (h[1] - py) / (vy - h[4])
                            if not t.is_integer() or t <= 0:
                                break
                        elif py != h[1]:
                            break
                    else:
                        yCandidates[(py, vy)] = True

    zCandidates = {}
    # find z candidates
    for i in range(0, 1000):
        for j in range(0, 20):
            for k in [-1, +1]:
                for l in [-1, +1]:
                    pz = (highZ - lowZ) // 2 + k * i
                    vz = 10 + l * j
                    for h in hailstones:
                        if vz - h[5] != 0:
                            t = (h[2] - pz) / (vz - h[5])
                            if not t.is_integer() or t <= 0:
                                break
                        elif pz != h[2]:
                            break

                    else:
                        zCandidates[(pz, vz)] = True

    for (px, vx) in xCandidates:
        for (py, vy) in yCandidates:
            for (pz, vz) in zCandidates:
                for h in hailstones:
                    tx = ty = tz = 0
                    if vx - h[3] != 0:
                        tx = (h[0] - px) / (vx - h[3])

                    if vy - h[4] != 0:
                        ty = (h[1] - py) / (vy - h[4])

                    if vz - h[5] != 0:
                        tz = (h[2] - pz) / (vz - h[5])
                    if tx == 0:
                        tx = max(ty, tz)
                    if ty == 0:
                        ty = max(tx, tz)
                    if tz == 0:
                        tz = max(tx, ty)
                    if tx == ty == tz:
                        print("Found solution at", px, vx, py, vy, pz, vz)
                        return px + py + pz


def part2solver(hailstones):
    ppx, ppy, ppz, vvx, vvy, vvz, t0, t1, t2 = symbols("ppx, ppy, ppz, vvx, vvy, vvz t0, t1, t2")

    h = hailstones
    r = sympy.solve(
        (ppx + vvx * t0 - h[0][0] - t0 * h[0][3],
         ppy + vvy * t0 - h[0][1] - t0 * h[0][4],
         ppz + vvz * t0 - h[0][2] - t0 * h[0][5],
         ppx + vvx * t1 - h[1][0] - t1 * h[1][3],
         ppy + vvy * t1 - h[1][1] - t1 * h[1][4],
         ppz + vvz * t1 - h[1][2] - t1 * h[1][5],
         ppx + vvx * t2 - h[2][0] - t2 * h[2][3],
         ppy + vvy * t2 - h[2][1] - t2 * h[2][4],
         ppz + vvz * t2 - h[2][2] - t2 * h[2][5]), ppx, ppy, ppz, vvx, vvy, vvz, t0, t1, t2, dict=True)

    result = r[0][ppx] + r[0][ppy] + r[0][ppz]
    return result


def solve(filename, lowerbound, upperbound):
    f = open(filename)

    hailstones = []
    while s := f.readline():
        l, r = s.split(" @ ")
        px, py, pz = map(int, l.split(", "))

        vx, vy, vz = map(int, r.split(", "))
        hailstones.append((px, py, pz, vx, vy, vz))

    result1 = part1(hailstones, lowerbound, upperbound)
    result2 = part2solver(hailstones)

    return result1, result2


start = time.time()

filename = "input/input24-sample.txt"
p1, p2 = solve(filename, 7, 27)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input24.txt"
p1, p2 = solve(filename, 200000000000000, 400000000000000)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
