import time
from math import gcd


def calcLCM(list):
    lcm = 1
    for m in list:
        lcm = lcm * m // gcd(lcm, m)
    return lcm


class Pulse:
    def __init__(self, source, dest, signal):
        self.source = source
        self.dest = dest
        self.signal = signal

    def __str__(self):
        return self.source + " -" + str(self.signal) + " -> " + self.dest


class Node:
    def __init__(self, name, op, queue, successors):
        self.name = name
        self.op = op
        self.successors = successors
        self.inputs = {}
        self.state = False
        self.queue = queue

    def hash(self):
        if self.op == "&":
            h = str(self.state)
            for v in self.inputs.values():
                h += str(v)
            return h

    def compute(self, pulse):
        match self.op:
            case "&":
                if pulse.source in self.inputs:
                    self.inputs[pulse.source] = pulse.signal
                else:
                    self.inputs[pulse.source] = False

                if all(i for i in self.inputs.values()):
                    self.state = False
                else:
                    self.state = True
                result = (self.state, not self.state)

            case "%":
                if not pulse.signal:
                    self.state = not self.state
                    result = (self.state, not self.state)
                else:
                    return (0, 0)

            case "broadcaster":
                self.state = False
                result = (0, 1)

            case noop if noop in ["rx", "output"]:
                return (0, 0)

        for s in self.successors:
            self.queue.append(Pulse(self.name, s, self.state))

        return (len(self.successors) * result[0], len(self.successors) * result[1])


def setup(filename):
    f = open(filename)
    machine = {}
    queue = []

    for line in f.readlines():
        name, successors = line.strip().split(" -> ")
        if name[0] in ["&", "%"]:
            op = name[0]
            name = name[1:]
        else:
            op = "broadcaster"
        machine[name] = Node(name, op, queue, successors.split(", "))

    machine["output"] = Node("output", "output", queue, [])
    machine["rx"] = Node("rx", "rx", queue, [])

    rx = False
    for name, node in machine.items():
        for s in node.successors:
            if machine[s].op == "&":
                machine[s].inputs[name] = False
            elif s == "rx":
                rx = True

    return machine, queue, rx


def part1(filename):
    machine, queue, rx = setup(filename)
    high = low = 0

    for i in range(1000):
        result = machine["broadcaster"].compute(None)
        low += 1 + result[1]  # for button press + broadcaster
        while queue:
            pulse = queue.pop(0)
            result = machine[pulse.dest].compute(pulse)
            high += result[0]
            low += result[1]

    return high * low


def part2(filename):
    machine, queue, rx = setup(filename)

    if not rx:
        return -1
    else:
        cyclenodes = ["fh", "fn", "hh", "lk"]
        cycles = {}
        statecache = {}
        for c in cyclenodes:
            cycles[c] = 0
            statecache[c] = {}

        cycle = 1
        while any(c == 0 for c in cycles.values()):
            result = machine["broadcaster"].compute(None)
            while queue:
                pulse = queue.pop(0)
                machine[pulse.dest].compute(pulse)
                for c in cyclenodes:
                    if machine[c].state:
                        if machine[c].hash() in statecache[c]:
                            cycles[c] = statecache[c][machine[c].hash()]
                        else:
                            statecache[c][machine[c].hash()] = cycle
            cycle += 1

        return calcLCM(cycles.values())


def solve(filename):
    result1 = part1(filename)
    result2 = part2(filename)
    return result1, result2


start = time.time()

filename = "input/input20-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input20.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
