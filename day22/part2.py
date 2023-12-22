
from collections import defaultdict, deque
from functools import cache
from itertools import chain, product, starmap
from more_itertools import consume
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

supports: dict[int, set[int]] = defaultdict(set) # this brick supports which bricks
ontopof: dict[int, set[int]] = defaultdict(set) # this brick is on top of?

for idx, xyslice, height in b:

    dz = heightmap[xyslice].max()

    # possible landing bricks
    p = brickmap[xyslice]
    if dz != 0:
        supp = p[heightmap[xyslice] == dz]
        supp = set(supp)
        ontopof[idx].update(supp)
        # set(supp) is the set of all bricks this brick rests on
        # hence naturally we have the "base closure" (idx -> bricks it rests on)
        # we want the opposite mapping (idx -> bricks resting on this
        consume(map(lambda x: supports[x].add(idx), supp))

        # if len(set(supp)) == 1:
        #     unsafe_br.add(supp[0])

    heightmap[xyslice] = dz + height
    brickmap[xyslice] = idx

# ontopof and supports are sufficient information to compute the "falling closure"
# A supports [X, Y, Z, ...]
# X, Y support B
# A supports B
# Y supports C, but F supports C but A does not support F

# step 1, calculate the supporting closure (who are ultimately supported)
# step 2 shake the tree (who are only supported by this?) (easy, we have ontopof)

@cache
def supportswho(idx):
    acc = {idx,}
    for i in supports[idx]:
        acc |= supportswho(i)
    return acc

# now we know idx supports which all nodes as a set

# falling closure
def falling(idx):
    resting_on_this = supportswho(idx)
    closure = resting_on_this.copy()
    for i in resting_on_this:
        if i not in closure or i == idx: continue
        if not ontopof[i].issubset(closure): # any nodes from outside? then drop i by shaking
            closure.difference_update(supportswho(i))
    return closure

# @cache
# def falling(idx):
#     acc = {idx,}
#     for i in supports[idx]: # for every brick this brick supports
#         if len(ontopof[i]) == 1 and idx in ontopof[i]:
#             acc |= falling(i)
#     return acc

print(mapper.of(range(1, totbricks + 1)) | falling | len | (lambda x: x-1) >= sum)