import time
from collections import defaultdict

def def_value():
    return 1

def solve(filename):
    result1 = 0
    result2 = 0

    f = open(filename)
    file = open(filename)

    current = 0

    lines = f.readlines()
    multiplier = cards = [1] * len(lines)

    for blocks in [s.strip().split(":")[1].split("|") for s in lines]:
        count = 0

        winning = set(blocks[0].split())
        having = set(blocks[1].split())

        count += len(winning & having)

        for i in range(count):
            multiplier[current+i+1] += multiplier[current]

        if(count>0):
            result1 += 2**(count-1)
        current +=1

    result2 = sum(multiplier)
    return result1, result2

start = time.time()
filename = "input/input04-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input04.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)



