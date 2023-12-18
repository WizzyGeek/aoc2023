from itertools import pairwise, product
from more_itertools import consume
import numpy as np
from wafle import mapper, star
import sys

dmap = {
    "U": -1+0j,
    "D": 1+0j,
    "R": 1j,
    "L": -1j
}

a = mapper.of(open("day18/input.txt", "r").readlines()) | str.strip | str.split | (lambda x: dmap[x[0]] * int(x[1]))

pos = 0 + 0j
mr, mi = 0.0, 0.0
mmr, mmi = 0.0, 0.0
v = [(0, 0)]
for dir in a:
    pos += dir
    v.append((int(pos.real), int(pos.imag)))
    mr, mi = max(pos.real, mr), max(pos.imag, mi)
    mmr, mmi = min(pos.real, mmr), min(pos.imag, mmi)

mr = int(mr + 1 - mmr)
mi = int(mi + 1 - mmi)

v = mapper.of(v) | star(lambda y, x: (int(y - mmr), int(x - mmi))) >= list
# print(mr, mi, v)

space = np.zeros((mr, mi), dtype=np.uint8)
# print(space)

@star
def assign_slice(x, y):
    if x[0] == y[0]:
        space[x[0], min(x[1], y[1]):(max(x[1], y[1]) + 1)] = 1
    else:
        space[min(x[0], y[0]):(max(x[0], y[0]) + 1), x[1]] = 1

def is_in(pos):
    return space[pos] == 1 or (bool(space[pos[0], pos[1]:].sum() % 2) and bool(space[pos[0],:pos[1]].sum() % 2) and bool(space[pos[0]:, pos[1]].sum() % 2) and bool(space[:pos[0], pos[1]].sum() % 2))

(mapper.of(v) > pairwise) | assign_slice >= consume

print("\n".join("".join((".","#")[j] for j in i) for i in space), file=open("day18/vis.txt", "w"))

al = [0] * space.shape[1]
space = np.vstack((al, space, al))
al = np.zeros((space.shape[0], 1), dtype=np.uint8)
space = np.hstack((al, space, al))

ly = len(space)
lx = len(space[0])
d = space
vis = dict()
def flood_fill(y, x):
    vis[(y, x)] = True
    if y < 0 or x < 0 or y >= ly or x >= lx or (d[y, x] == 1 or d[y, x] == 2):
        return

    d[y, x] = 2

    (y + 1, x) not in vis and flood_fill(y + 1, x)
    (y, x + 1) not in vis and flood_fill(y, x + 1)
    (y + 1, x + 1) not in vis and flood_fill(y + 1, x + 1)
    (y - 1, x) not in vis and flood_fill(y - 1, x)
    (y, x - 1) not in vis and flood_fill(y, x - 1)
    (y - 1, x - 1) not in vis and flood_fill(y - 1, x - 1)
    (y - 1, x + 1) not in vis and flood_fill(y - 1, x + 1)
    (y + 1, x - 1) not in vis and flood_fill(y + 1, x - 1)

sys.setrecursionlimit(422 * 380 + 100)

flood_fill(0, 0)

# print("\n".join("".join((".","#","O")[j] for j in i) for i in space), file=open("day18/vis2.txt", "w"))
print("\n".join("".join((".",".","O")[j] for j in i) for i in space).count("."))