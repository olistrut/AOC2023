import time
from collections import defaultdict

def def_value():
    return []

def solve(filename):

    text = open(filename).read().split("\n\n")

    maps = defaultdict(def_value)

    seeds = list(map(int,text[0].split(":")[1].strip().split(" ")))
    for i, section in enumerate( ["seed2Soil", "soil2Fertilizer", "fertilizer2water",  "water2Light", "light2Temp", "temp2Humidity", "humidity2Location"]):
        for line in text[i+1].strip().split(":\n")[1].split("\n"):
            seed, soil, l = list(map(int, line.split(" ")))
            maps[section].append((seed, soil, l))

    result1 = calculate(seeds, maps)
    result2 = min([binSearch(maps, seeds[i], seeds[i] + seeds[i + 1]) for i in range(0,len(seeds),2)])

    return result1, result2


def binSearch(maps, start, end):
    r1 = calculate([start], maps)
    r2 = calculate([end], maps)

    if r2-r1 == end-start:
        # found a range where calculate(seed) increases linearly with seed
        return r1
    else:
        # otherwise continue binary search
        mid = (start + end) // 2
        return(min(binSearch(maps, start, mid), binSearch(maps, mid + 1, end)))

def calculate(seeds, maps):
    chains = defaultdict(def_value)
    for s in seeds:
        chains[s] = [None] * 8

        chains[s][0] = s
        for i, transformation in enumerate(maps):
            # print("Finding transformation ", i, "-", transformation, "for seed", s, "and start", chains[s][i])
            chains[s][i + 1] = chains[s][i]
            start = chains[s][i]
            for destinationStart, sourceStart, range in maps[transformation]:
                if sourceStart <= start < sourceStart + range:
                    chains[s][i + 1] = destinationStart + (start - sourceStart)
            # print("Found a final destination for seed ", s, "at", chains[s][i + 1])

    result1 = min(chain[7] for chain in chains.values())

    return result1


start = time.time()
filename = "input/input05-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input05.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)



