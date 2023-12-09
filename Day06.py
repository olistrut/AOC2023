import time
import math


def solve(filename):
    f = open(filename)

    times = list(map(int, f.readline().split(":")[1].split()))
    distances = list(map(int, f.readline().split(":")[1].split()))

    result1 = calc(times, distances)

    times = [int(''.join([str(t) for t in times]))]
    distances = [int(''.join([str(d) for d in distances]))]

    result2 = calc(times, distances)
    return result1, result2


def calc(times, distances):
    result = 1
    for t, d in zip(times, distances):
        accel1 = t/2 + math.sqrt(t**2/4-d)
        accel2 = t/2 - math.sqrt(t**2/4-d)

        if not accel1.is_integer():
            accel1 = math.floor(accel1)
        else:
            accel1 = accel1-1
        if not accel2.is_integer():
            accel2 = math.ceil(accel2)
        else:
            accel2 = accel2+1

        result *= int(accel1-accel2+1)

    return result


start = time.time()
filename = "input/input06-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input06.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
