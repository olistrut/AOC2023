import time
from collections import defaultdict


transformations = ["seed2Soil", "soil2Fertilizer", "fertilizer2water",  "water2Light", "light2Temp", "temp2Humidity", "humidity2Location"]


def def_value():
    return []

def solve(filename):

    text = open(filename).read().split("\n\n")
    maps = defaultdict(def_value)

    seeds = list(map(int, text[0].split(":")[1].strip().split(" ")))
    for i, section in enumerate(transformations):
        for line in text[i+1].strip().split(":\n")[1].split("\n"):
            seed, soil, l = list(map(int, line.split(" ")))
            maps[section].append((seed, soil, l))

    result1 = part1(seeds, maps)
    result2 = min([part2(0,maps, seeds[i], seeds[i] + seeds[i + 1]) for i in range(0,len(seeds),2)])

    return result1, result2

def part2(level, maps, start, end):
    transformation = transformations[level]
    # print("Working at level:  ", level,"which is",transformation)

    rangeQueue =  [(start, end)]
    nextLevelQueue = []

    for destinationStart, sourceStart, r in maps[transformation]:
        sourceEnd = sourceStart + r
        #print("Source r: ", sourceStart, sourceEnd)
        #print("Destination :", destinationStart, destinationStart + r)

        newRangeQueue = []
        while(rangeQueue):
            start, end = rangeQueue.pop()

            #print("Input r: ", start, end)

            before = (start, min(sourceStart, end))
            after = (max(start, sourceEnd), end)
            middle = (max(start, sourceStart), min(end, sourceEnd))

            if before[0]<before[1] :
                newRangeQueue.append(before)
                #print("New before range: ", before)
            if after[1]>after[0] :
                newRangeQueue.append(after)
                #print("New after range: ", before)
            if middle[1]>middle[0]:
                nextLevelQueue.append((middle[0]-sourceStart+destinationStart, -sourceStart+destinationStart+middle[1] ))
                #print("New middle range: ", middle, "mapped to ",(middle[0]-sourceStart+destinationStart, -sourceStart+destinationStart+middle[1] ))
        rangeQueue += newRangeQueue

    nextLevelQueue += rangeQueue

    if transformation != "humidity2Location":
        result = min([part2(level+1, maps, start, end) for (start, end) in nextLevelQueue])
    else:
       result = min([start for (start, end) in nextLevelQueue])

    return result


def part1(seeds, maps):
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
