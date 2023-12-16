import time


def calcHash(s):
    h = 0
    for c in s:
        h = ((h + ord(c)) * 17) % 256
    return h


def solve(filename):
    f = open(filename)
    result1 = result2 = 0
    boxes = [{} for _ in range(256)]

    for s in f.read().strip().split(","):
        h = calcHash(s)
        result1 += h

        if s[-1] == "-":
            lens = s[:-1]
            target = calcHash(lens)
            if lens in boxes[target]:
                del boxes[target][lens]
        else:
            lens, strength = s.split("=")
            boxes[calcHash(lens)][lens] = int(strength)

    for i, b in enumerate(boxes, 1):
        for j, (lens, strength) in enumerate(b.items(), 1):
            result2 += i * j * int(strength)

    return result1, result2


start = time.time()
filename = "input/input15-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input15.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
