
from itertools import chain, product, starmap
import numpy as np
from wafle import mapper, rpartial, star


a = mapper.of(open("day22/input.txt", "r").readlines()) | rpartial(str.split, "~")
a |= star(lambda x, y: (tuple(map(int, x.split(","))), tuple(map(lambda k: int(k) + 1, y.split(",")))))
a = a >= list

d = mapper.of(a)
d |= star(lambda _, t: (t[0], t[1]))
shape = d >= max

# print(d)

c = mapper.of(a)
c |= lambda x: tuple(starmap(slice, zip(*x)))


def brick_vertical(brick: list):
    return brick[-1].start + 1 != brick[-1].stop

b = mapper.of(sorted(c, key=lambda brick: brick[-1].start))
b = b > enumerate
b |= star(lambda idx, x: (idx + 1, x[:-1], x[-1].stop - x[-1].start))

# print(b >= list)

totbricks = len(a)

heightmap = np.zeros(shape, dtype=np.uint32)
brickmap = np.zeros(shape, dtype=np.uint16) # top brick of ever cell

unsafe_br = set()

for idx, xyslice, height in b:

    dz = heightmap[xyslice].max()

    # possible landing bricks
    p = brickmap[xyslice]
    if dz != 0:
        supp = p[heightmap[xyslice] == dz]
        if len(set(supp)) == 1:
            unsafe_br.add(supp[0])

    heightmap[xyslice] = dz + height
    brickmap[xyslice] = idx

print(totbricks - len(unsafe_br))