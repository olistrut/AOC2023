import time
import itertools


def symmetry(rows, default = 0):
    result = []

    for div in range(1, len(rows)):
        length = min(div, len(rows) - div)
        b1 = rows[div - length:div]
        b2 = rows[div:div + length]
        b2.reverse()
        if b1 == b2:
            result.append(div)

    if not result: result.append(default)
    return result


def bitFlip(block, x, y):
    if block[y][x] == '#':
        block[y][x] = "."
    else:
        block[y][x] = '#'


def solve(filename):
    result1 = result2 = 0
    f = open(filename)
    blocks = f.read().strip().split("\n\n")

    for b in blocks:
        rows = [list(row) for row in b.split("\n")]
        cols = list(map(list, zip(*rows)))

        symY = symmetry(rows)[0]
        symX = symmetry(cols)[0]

        result1 += symY * 100 + symX

        for (x, y) in itertools.product(range(len(rows[0])), range(len(rows))):
            bitFlip(rows, x, y)
            cols = list(map(list, zip(*rows)))

            if syms := [s for s in symmetry(cols, symX) if s != symX]:
                result2 += syms[0]
                break

            if syms := [s for s in symmetry(rows, symY) if s != symY]:
                result2 += syms[0] * 100
                break

            bitFlip(rows, x, y)

    return result1, result2


start = time.time()
filename = "input/input13-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input13.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
