import time

def solve(filename, translate):
    file = open(filename)
    lines = file.read().split("\n")
    sum = 0

    for line in lines:
       #numbers = [(i, c) for i, c in enumerate(line) if c.isdigit()]
       #if (len(numbers)>0):
       # c1 = numbers[0][1]
       # c2 = numbers[len(numbers)-1][1]
       #sum += int(c1) *10 + int(c2)

        if (len(line)>0):
            digits = list(translate.keys())

            index = []
            i = 0
            while i in range(len(line)):
                index += [digits[j] for j in range(len(digits)) if line[i:].startswith(digits[j])]
                i += 1

            min_val = translate[index[0]]
            max_val = translate[index[-1]]

            sum += min_val * 10 + max_val

    return sum


start = time.time()
translate_p1 = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}
translate_p2 = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}


filename = "input/input1-sample.txt"
p1 = solve(filename, translate_p1)
print("Part 1 (Example 1): ", p1)

filename = "input/input1-sample2.txt"
p2 = solve(filename,  translate_p2)
print('Part 2 (Example 2): ', p2)


filename = "input/input1.txt"

p1 = solve(filename, translate_p1 )
p2 = solve(filename, translate_p2)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)
print("Total time: ", time.time() - start)
