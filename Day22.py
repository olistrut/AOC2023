import time
from collections import defaultdict


def def_value_dict():
    return {}


def overlap(list1, list2, dimensions):
    # assumes list is x1 start, x2 start, ..., x1 end, x2 end, ...
    for c in dimensions:
        if max(list1[c], list2[c]) > min(list1[c + len(list1) // 2], list2[c + len(list1) // 2]):
            return False
    return True


def solve(filename):
    f = open(filename)
    result1 = result2 = 0

    bricks = []

    maxZ = -1
    for i, coordinates in enumerate(f.readlines()):
        brick = list(map(int, coordinates.replace("~", ",").strip().split(",")))
        brick.append(i)
        bricks.append(brick)
        if brick[5] > maxZ:
            maxZ = brick[5]

    # sort bricks by lower y value to reduce search work in dropping bricks
    bricks.sort(key=lambda l: l[2])

    # drop
    for i, brick in enumerate(bricks):
        drop = brick[2] - 1
        for j in range(i):
            obstacle = bricks[j]
            if overlap(brick, obstacle, [0, 1]):

                if brick[2] > obstacle[5]:
                    # bring down brick to potential obstacle
                    distance = brick[2] - obstacle[5]
                    drop = min(distance - 1, drop)
        brick[2] -= drop
        brick[5] -= drop

    bricks.sort(key=lambda l: l[2])

    # check for removal possibility
    incoming = [0] * len(bricks)  # stores how many supporting pillars we have for each brick
    outgoing = defaultdict(def_value_dict) # for each brick b holds a dictionary of other bricks supported by b

    for i, brick in enumerate(bricks):
        # find all bricks with lower y bound 1 above brick upper y bound. we are sorted by lower y bound, so this can only be above
        j = i + 1
        while j < len(bricks) and bricks[j][2] <= brick[5]:
            j += 1
        while j < len(bricks) and bricks[j][2] == brick[5] + 1:
            # found a possible ceiling - check x/y overlap
            if overlap(bricks[j], brick, [0, 1]):
                incoming[j] += 1
                outgoing[i][j] = True
            j += 1

    removable = {}
    for i in range(len(bricks)):
        if len(outgoing[i]) == 0:
            removable[i] = True
        else:
            candidate = True
            for ceiling in outgoing[i]:
                if incoming[ceiling] < 2:
                    candidate = False
            if candidate:
                removable[i] = True

    result1 = len(removable)

    candidates = set(range(len(bricks))).difference(set(removable.keys()))
    for c in candidates:
        pillars = list(incoming)
        queue = [c]

        destroyed = {}
        while queue:
            current = queue.pop(0)

            # print("  Checking block ", current)
            if current not in destroyed:
                if pillars[current] == 0 and current != c:
                    # print("    -> Block", current,"can be destroyed")
                    destroyed[current] = True
                    result2 += 1

                if pillars[current] == 0 or current == c:
                    if len(outgoing[current]) > 0:
                        for new in outgoing[current].keys():
                            # print("    -> Removing support for ", new, "and removing pillar from", current, "to", new)
                            queue.append(new)
                            pillars[new] -= 1

    return result1, result2


start = time.time()

filename = "input/input22-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input22.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)

# 88516 is too high
# 1300 is too low
