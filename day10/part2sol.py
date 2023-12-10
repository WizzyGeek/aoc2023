

import sys


with open("day10/proc3.txt", "r") as fp:
    d = list(map(lambda k: list(k[:-1] + " "), fp.readlines()))

vis = {}

ly = len(d)
lx = len(d[0])
def flood_fill(y, x):
    vis[(y, x)] = True
    if y < 0 or x < 0 or y >= ly or x >= lx or (d[y][x] in {"|", "-", "L", "S", "F", "J", "7", "O"}):
        return

    d[y][x] = "O"

    (y + 1, x) not in vis and flood_fill(y + 1, x)
    (y, x + 1) not in vis and flood_fill(y, x + 1)
    (y + 1, x + 1) not in vis and flood_fill(y + 1, x + 1)
    (y - 1, x) not in vis and flood_fill(y - 1, x)
    (y, x - 1) not in vis and flood_fill(y, x - 1)
    (y - 1, x - 1) not in vis and flood_fill(y - 1, x - 1)
    (y - 1, x + 1) not in vis and flood_fill(y - 1, x + 1)
    (y + 1, x - 1) not in vis and flood_fill(y + 1, x - 1)

sys.setrecursionlimit(2000000)
flood_fill(0, 0)

print("\n".join(map("".join, d)), file=open("ret.txt", "w"))

print(("\n".join(map(lambda r: "".join(map(lambda b: b[1], (filter(lambda k: k[0] % 2 == 0, enumerate(r[1]))))), filter(lambda k: k[0] % 2 == 0, enumerate(d))))).count("."))