import time
import itertools
from copy import deepcopy
from collections import defaultdict


def def_value():
    return "."


def tiltUp(board, width, height):
    for pos in ((x,y) for y in range(1, height) for x in range(width)): # we don't need to try to shift up the first row
        while board[pos] == "O" and 0 <= pos[1] -1 and board[(pos[0], pos[1] - 1)] == ".":
            board[pos] = "."
            pos = (pos[0], pos[1] - 1)
            board[pos] = "O"
    return board


def cycle(board, width, height):
    for pos in ((x,y) for y in range(1, height) for x in range(width)): # we don't need to try to shift up the first row
        while board[pos] == "O" and 0 <= pos[1] - 1 and board[(pos[0], pos[1] - 1)] == ".":
            board[pos] = "."
            pos = (pos[0], pos[1] - 1)
            board[pos] = "O"

    for pos in ((x,y) for x in range(1, width) for y in range(height)):
        while board[pos] == "O" and 0 <= pos[0] - 1 and board[(pos[0] - 1, pos[1])] == ".":
            board[pos] = "."
            pos = (pos[0] - 1, pos[1])
            board[pos] = "O"

    for pos in ((x,y) for y in range(height - 2, -1, -1) for x in range(width)):
        while board[pos] == "O" and pos[1] + 1 < height and board[(pos[0], pos[1] + 1)] == ".":
            board[pos] = "."
            pos = (pos[0], pos[1] + 1)
            board[pos] = "O"

    for pos in ((x,y) for x in range(width - 2, -1, -1) for y in range(height)):
        while board[pos] == "O" and pos[0] + 1 < width and board[(pos[0] + 1, pos[1])] == ".":
            board[pos] = "."
            pos = (pos[0] + 1, pos[1])
            board[pos] = "O"

    return board


def printBoard(board, width, height):
    for y in range(height):
        for x in range(width):
            print(board[(x, y)], end="")
        print()
    print()


def calcWeight(board, height):
    weight = 0
    for pos, value in [(p, v) for p, v in board.items() if v == "O"]:
        weight += height - pos[1]
    return weight


def hash(board):
    return str(board.values())

def solve(filename):
    f = open(filename)
    board = defaultdict(def_value)

    for height, s in enumerate(f.readlines(), 1):
        for width, c in enumerate(s.strip(), 1):
            board[(width-1, height-1)] = c

    result1 = calcWeight(tiltUp(deepcopy(board), width, height), height)

    cache = {}
    for i in range(1, 500):
        board = cycle(board, width, height)
        if (hash(board)) in cache:
            if (1000000000 - i) % (i - cache[hash(board)]) == 0:
                result2 = calcWeight(board, height)
                break
        else:
            cache[hash(board)] = i

    return result1, result2


start = time.time()
filename = "input/input14-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)
# 107053 is too high

filename = "input/input14.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)

print("Total time: ", time.time() - start)
