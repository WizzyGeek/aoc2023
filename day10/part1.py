import sys

vis = {}

pp = open("log.txt", "w")

def loop(y, x, d):
    t = d[y][x]
    print(t, y + 1, x + 1, file=pp)

    if vis.get((y, x)):
        print("loop", y, x)
        return 0

    if t == "S":
        print(y, x)
        if vis.get((y, x)):
            return 1
        vis[(y, x)] = True
        return loop(y, x - 1, d) + 1

    vis[(y, x)] = True

    if t == "-" and vis.get((y, x + 1)):
        return loop(y, x - 1, d) + 1
    if t == "-" and vis.get((y, x - 1)):
        return loop(y, x + 1, d) + 1
    if t == "|" and vis.get((y - 1, x)):
        return loop(y + 1, x, d) + 1
    if t == "|" and vis.get((y + 1, x)):
        return loop(y - 1, x, d) + 1
    if t == "7" and vis.get((y, x - 1)):
        return loop(y + 1, x, d) + 1
    if t == "7" and vis.get((y + 1, x)):
        return loop(y, x - 1, d) + 1
    if t == "F" and vis.get((y + 1, x)):
        return loop(y, x + 1, d) + 1
    if t == "F" and vis.get((y, x + 1)):
        return loop(y + 1, x, d) + 1
    if t == "L" and vis.get((y - 1, x)):
        return loop(y, x + 1, d) + 1
    if t == "L" and vis.get((y, x + 1)):
        return loop(y - 1, x, d) + 1
    if t == "J" and vis.get((y - 1, x)):
        return loop(y, x - 1, d) + 1
    if t == "J" and vis.get((y, x - 1)):
        return loop(y - 1, x, d) + 1

    print(t, y, x, d)
    raise Exception

with open("day10/input.txt", "r") as fp:
    d = list(map(str.strip, fp.readlines()))

sys.setrecursionlimit(100000)
try:
    print(loop(86, 89, d))
except:
    pass

print(len(vis))