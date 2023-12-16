import time
from copy import deepcopy


def def_value():
    return "."


def tiltUp(board, width, height):
    for xx,yy in ((x,y) for y in range(1, height) for x in range(width)): # we don't need to try to shift up the first row
        while board[xx][yy] == "O" and 0 <= yy -1 and board[xx][yy-1] == ".":
            board[xx][yy] = "."
            yy -= 1
            board[xx][yy] = "O"
    return board


def cycle(board, width, height):
    for (xx,yy) in [(x,y) for y in range(1, height) for x in range(width)]: # we don't need to try to shift up the first row
        while board[xx][yy] == "O" and 0 <= yy - 1 and board[xx][yy-1] == ".":
            board[xx][yy] = "."
            yy -= 1
            board[xx][yy] = "O"

    for (xx,yy) in [(x,y) for x in range(1, width) for y in range(height)]:
        while board[xx][yy] == "O" and 0 <= xx - 1 and board[xx-1][yy] == ".":
            board[xx][yy] = "."
            xx -= 1
            board[xx][yy] = "O"

    for (xx,yy) in [(x,y) for y in range(height - 2, -1, -1) for x in range(width)]:
        while board[xx][yy] == "O" and yy + 1 < height and board[xx][yy+1] == ".":
            board[xx][yy] = "."
            yy += 1
            board[xx][yy] = "O"

    for (xx,yy) in [(x,y) for x in range(width - 2, -1, -1) for y in range(height)]:
        while board[xx][yy] == "O" and xx + 1 < width and board[xx + 1][yy] == ".":
            board[xx][yy] = "."
            xx += 1
            board[xx][yy] = "O"

    return board


def printBoard(board, width, height):
    for y in range(height):
        for x in range(width):
            print(board[x][y], end="")
        print()
    print()


def calcWeight(board, width, height):
    weight = 0
    for y in range(height):
        for x in range(width):
            if board[x][y] == "O":
                weight += height - y
    return weight


def hash(board):
    return str(board)

def solve(filename):
    f = open(filename)
    board = []

    for height, s in enumerate(f.readlines(), 1):
        board.append([])
        for width, c in enumerate(s.strip(), 1):
            board[height-1].append(c)

    board = list(map(list, zip(*board)))
    result1 = calcWeight(tiltUp(deepcopy(board), width, height), width, height)

    cache = {}
    for i in range(1, 500):
        board = cycle(board, width, height)
        if (hash(board)) in cache:
            if (1000000000 - i) % (i - cache[hash(board)]) == 0:
                result2 = calcWeight(board, width, height)
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
