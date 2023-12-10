import sys

vis = {}

def loop(y, x, d):
    t = d[2 * y][2 * x]
    a = 2 * y
    b = 2 * x
    # print(a, b)

    if vis.get((y, x)):
        print("loop")
        return 0

    if t == "S":
        print(y, x)
        if vis.get((y, x)):
            return 1
        vis[(y, x)] = True
        d[a][b - 1] = "-"
        return loop(y, x - 1, d) + 1

    vis[(y, x)] = True

    if t == "-" and vis.get((y, x + 1)):
        d[a][b - 1] = "-"
        return loop(y, x - 1, d) + 1
    if t == "-" and vis.get((y, x - 1)):
        d[a][b + 1] = "-"
        return loop(y, x + 1, d) + 1
    if t == "|" and vis.get((y - 1, x)):
        d[a + 1][b] = "|"
        return loop(y + 1, x, d) + 1
    if t == "|" and vis.get((y + 1, x)):
        d[a - 1][b] = "|"
        return loop(y - 1, x, d) + 1
    if t == "7" and vis.get((y, x - 1)):
        d[a + 1][b] = "|"
        return loop(y + 1, x, d) + 1
    if t == "7" and vis.get((y + 1, x)):
        d[a][b - 1] = "-"
        return loop(y, x - 1, d) + 1
    if t == "F" and vis.get((y + 1, x)):
        d[a][b + 1] = "-"
        return loop(y, x + 1, d) + 1
    if t == "F" and vis.get((y, x + 1)):
        d[a + 1][b] = "|"
        return loop(y + 1, x, d) + 1
    if t == "L" and vis.get((y - 1, x)):
        d[a][b + 1] = "-"
        return loop(y, x + 1, d) + 1
    if t == "L" and vis.get((y, x + 1)):
        d[a - 1][b] = "|"
        return loop(y - 1, x, d) + 1
    if t == "J" and vis.get((y - 1, x)):
        d[a][b - 1] = "-"
        return loop(y, x - 1, d) + 1
    if t == "J" and vis.get((y, x - 1)):
        d[a - 1][b] = "|"
        return loop(y - 1, x, d) + 1

    print(t, y, x, d)
    raise Exception

# for r, i in enumerate(d):
#     for c, j in enumerate(i):
#         if vis.get((r, c)):
#             print(j, end="")
#         else:
#             print(".", end="")
#     print()

with open("day10/proc2.txt", "r") as fp:
    d = list(map(lambda k: list(k[:-1]), fp.readlines()))
    # d = list(map(" ".join, d))
    # d = ("\n " + " " * len(d[0]) + "\n").join(d)
    # print(d, file=open("proc2.txt", "w"))

# print(len(d), len(d[0]), d)

sys.setrecursionlimit(20000000)
try:
    print(loop(86, 89, d))
except:
    raise

print("\n".join(map("".join, d)), file=open("proc3.txt", "w"))