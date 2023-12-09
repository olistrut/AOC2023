import time
import re
import itertools
from math import gcd


def calc(nums):
    diffs = [nums[i+1]-nums[i] for i in range(len(nums)-1)]

    if diffs == [0]*len(diffs):
        return nums[-1], nums[0]
    else:
        c1, c2 = calc(diffs)
        return c1 + nums[-1], nums[0] - c2


def solve(part, filename):
    result1 = 0
    result2 = 0

    f = open(filename)
    lines = f.read().strip().split("\n")

    for l in lines:
        r1, r2 = calc(list(map(int, l.strip().split())))
        result1 += r1
        result2 += r2

    return result1, result2

start = time.time()
filename = "input/input09-sample.txt"
p1, p2 = solve(1, filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input09.txt"
p1, p2 = solve(1, filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
