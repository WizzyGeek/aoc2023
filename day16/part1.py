import pprint
import sys
import numpy as np
import time

sys.setrecursionlimit(110 * 110 + 10)


with open("day16/input.txt", "r") as fp:
    d = list(map(lambda k: list(k.strip()), fp.readlines()))

d = np.array(d)

_n = time.time()
def in_bounds(x):
    return x[0] >= 0 and x[1] >= 0 and x[0] < d.shape[0] and x[1] < d.shape[1]

visited = set()

noloop = set()

def pred_next(sy, curr, last):
    dy, dx = curr[0] - last[0], curr[1] - last[1]
    if sy == "." or (sy == "|" and dy != 0) or (sy == "-" and dx != 0):
        yield curr[0] + dy, curr[1] + dx
    elif sy == "/":
        dy, dx = -1 * dx, -1 * dy
        yield curr[0] + dy, curr[1] + dx
    elif sy == "\\":
        yield curr[0] + dx, curr[1] + dy
    elif sy == "|" and dx != 0:
        yield curr[0] + 1, curr[1]
        yield curr[0] - 1, curr[1]
    elif sy == "-" and dy != 0:
        yield curr[0], curr[1] + 1
        yield curr[0], curr[1] - 1
    else:
        print(sy, curr, next)
        raise Exception()

def visit(curr, last):
    if (curr, last) in noloop:
        return

    if in_bounds(curr):
        visited.add(curr)
        noloop.add((curr, last))
    else: return

    sy = d[curr]

    for i in pred_next(sy, curr, last):
        visit(i, curr)

visit((0, 0), (0, -1))
print(len(visited))
print("Predicted time for part 2:", (time.time() - _n) * 110 * 4)
# print(d)
# pprint.pprint(visited)