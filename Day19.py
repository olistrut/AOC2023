import time
import re

class Part:
    def __init__(self, s):
        self.data = {}
        s = s[1:-1]
        s = s.split(",")
        for pair in s:
            name, value = pair.split("=")
            self.data[name] = int(value)

    def value(self):
        return sum(v for v in self.data.values())


class Branch:
    def __init__(self, operation, a, b, target):
        self.a = a
        self.operation = operation
        self.b = b
        self.target = target


class Workflow:
    def __init__(self, s):
        self.name, s = s.split("{")
        self.branches = []

        for r in s[:-1].split(","):
            m = re.search("([a-zA-Z]+)([<>]+)([0-9]*):([a-zA-Z]*)", r)
            if m:
                # if or elif branch
                self.branches.append(Branch(m.group(2), m.group(1), int(m.group(3)), m.group(4)))
            else:
                # else branch
                self.branches.append(Branch("else", "", 0, r))


def computeStep(workflows, workflow, part):
    for branch in workflows[workflow].branches:
        operation = branch.operation

        if operation != "else":
            op1 = part.data[branch.a]
            op2 = branch.b

            match operation:
                case "<":
                    if op1 < op2:
                        return branch.target
                case ">":
                    if op1 > op2:
                        return branch.target
        else:
            return branch.target



def part1(workflows, parts):
    result = 0
    for part in parts:
        workflow = "in"
        # print("Evaluating part", part)

        while workflow != "A" and workflow != "R":
            # print("Working in workflow", workflow)
            workflow = computeStep(workflows, workflow, part)

        if workflow == "A":
            # print("Found accepted for part ", part)
            result += part.value()

    return result


def part2(workflows, start, ranges, level):
    # prefix = level * " "
    # print(prefix, "Testing at level", level,"for",ranges,". - Starting at node",start)

    if start == "A":
        # print(prefix, "Found target A for", ranges)
        return (ranges["x"][1] - ranges["x"][0] + 1) * (ranges["m"][1] - ranges["m"][0] + 1) * (ranges["a"][1] - ranges["a"][0] + 1) * (ranges["s"][1] - ranges["s"][0] + 1)
    elif start == "R":
        return 0

    result = 0

    for branch in workflows[start].branches:
        # print(prefix, "> Testing branch", branch.a, "at level", level, "for", ranges, "in node ", start)
        match branch.operation:
            case "<":
                if ranges[branch.a][0] < int(branch.b) and ranges[branch.a][1] < int(branch.b):
                    # range fits entirely - do nothing and move on
                    continue
                elif ranges[branch.a][0] < int(branch.b) <= ranges[branch.a][1]:
                    # partial fit - partition range and go into recursion for fitting part of the range

                    r1 = dict(ranges)
                    r1[branch.a] = [ranges[branch.a][0], int(branch.b) - 1]
                    result += part2(workflows, branch.target, r1, level + 1)
                    # for non fitting part, move to next branch
                    ranges[branch.a] = [int(branch.b), ranges[branch.a][1]]

            case ">":
                if ranges[branch.a][0] > int(branch.b) and ranges[branch.a][1] > int(branch.b):
                    # range fits entirely - do nothing and move on
                    continue
                elif ranges[branch.a][0] <= int(branch.b) < ranges[branch.a][1]:
                    r1 = dict(ranges)
                    r1[branch.a] = [int(branch.b) + 1, ranges[branch.a][1]]

                    ranges[branch.a] = [ranges[branch.a][0], int(branch.b)]
                    result += part2(workflows, branch.target, r1, level + 1)

            case "else":
                # else branch
                result += part2(workflows, branch.target, ranges, level + 1)

    return result


def solve(filename):
    f = open(filename)
    parts = []
    workflows = {}

    s1, s2 = f.read().strip().split("\n\n")

    for s in s1.split("\n"):
        workflow = Workflow(s)
        workflows[workflow.name] = workflow

    for s in s2.split("\n"):
        parts.append(Part(s))

    result1 = part1(workflows, parts)
    result2 = part2(workflows, "in", {"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}, 0)

    return result1, result2


start = time.time()

filename = "input/input19-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input19.txt"
p1, p2 = solve(filename)

print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
