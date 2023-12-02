import time

def solve(filename):
    result1 = 0
    result2 = 0

    f = open(filename)
    file = open(filename)

    red = 12
    green = 13
    blue = 14

    while s := f.readline():
        game_num, game_content = s.split(":")
        game_num = int(game_num[4:])

        # print("Number:", game_num)

        sets = game_content.strip().split(";")
        possible = True

        min = {}
        min["red"] = 0
        min["blue"] = 0
        min["green"] = 0

        for set in sets:
            set_contents = set.split(",")

            for content in set_contents:
                count, color = content.strip().split(" ")
                count = int(count)
                if count > min[color]:
                    min[color] = count


        result2 += min["red"] * min["blue"] * min["green"]

        if (color == "red" and count > red) or (color == "blue" and count > blue)  or (color == "green" and count > green):
            possible = False

        if possible:
            # print("Set ", game_num, " is possible")
            result1 += game_num
        # else:
        #   print ("Set ", game_num, " is not possible")

    return result1, result2


start = time.time()
filename = "input/input2-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input2.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)
print("Total time: ", time.time() - start)
