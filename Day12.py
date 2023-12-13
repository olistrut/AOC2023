import time
import itertools


def isValid(s, descriptions):
    s += "."
    inDamage = False
    count = 0
    for i, c in enumerate(s):
        if c == "#":
            if not inDamage:
                start = i
                inDamage = True
        elif inDamage and c != "#":
            inDamage = False
            if count >= len(descriptions) or (i - start) != descriptions[count]:
                return False
            else:
                count += 1

    if count == len(descriptions):
        return True
    else:
        return False


cache = {}


def part2(s, descriptions):
    l = len(s)

    ss = sum(descriptions) + len(descriptions)
    if l < ss - 1:
        return 0

    s = s + "."

    if len(s) > 5 and len(descriptions) > 1:
        if s + str(descriptions) in cache:
            return cache[s + str(descriptions)]



    count = 0
    tokenStart = 0
    r1 = r2 = 0

    inDamage = False
    for i, c in enumerate(s):

        if c == "?":
            if not inDamage: tokenStart = i
            if count < len(descriptions) and i - tokenStart + 1 <= descriptions[count]:
                # -1 at the end to chop of "."
                r1 = part2(s[tokenStart:i] + "#" + s[i + 1:-1], descriptions[count:])

            r2 = part2(s[tokenStart:i] + "." + s[i + 1:-1], descriptions[count:])

            if len(s) > 5 and len(descriptions) > 1:
                cache[s + str(descriptions)] = r1 + r2

            return r1 + r2

        elif c == "#":
            if not inDamage:
                inDamage = True
                tokenStart = i

        elif c == ".":
            if inDamage:
                count += 1
                if not isValid(s[:i], descriptions[:count]):
                    return 0
                else:
                    r1 = part2(s[i + 1:-1], descriptions[count:])
                    if len(s) > 5 and len(descriptions) > 1:
                        cache[s + str(descriptions)] = r1
                    return r1

    if count == len(descriptions):
        return 1
    else:
        return 0


def part1(s, descriptions):
    result = 0
    locations = [i for i, c in enumerate(s) if c == "?"]

    blockCount = s.count("#")
    descSum = sum(descriptions)
    q = s.count("?")

    for combination in itertools.product(["#", "."], repeat=q):
        if combination.count("#") + blockCount != descSum:
            continue

        tmpS = s
        for i, c in enumerate(combination):
            tmpS = tmpS[:locations[i]] + c + tmpS[locations[i] + 1:]

        if isValid(tmpS, descriptions):
            result += 1

    return result


def solve(filename):
    result1 = result2 = 0
    f = open(filename)
    lines = f.read().strip().split("\n")
    for i, line in enumerate(lines):
        s, description = line.strip().split(" ")

        descriptions = list(map(int, description.split(",")))
        result1 += part1(s, descriptions)

        # part 2
        r = part2(s + "?" + s + "?" + s + "?" + s + "?" + s, descriptions * 5)
        result2 += r

    return result1, result2


start = time.time()
filename = "input/input12-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input12.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
