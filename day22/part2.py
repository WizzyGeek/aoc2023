
from collections import defaultdict
from functools import cache
from itertools import starmap
from time import time

from more_itertools import consume
from wafle import mapper, rpartial, star
import numpy as np


_n = time()

a = mapper.of(open("day22/input.txt", "r").readlines())
a |= rpartial(str.split, "~")
a |= star(lambda x, y: (tuple(map(int, x.split(","))), tuple(map(lambda k: int(k) + 1, y.split(",")))))
a = a >= list # all the cubes

d = mapper.of(a)
d |= star(lambda _, t: (t[0], t[1]))
shape = d >= max # find length of required x, y

c = mapper.of(a)
c |= lambda x: tuple(starmap(slice, zip(*x))) # convert our cubes to slices numpy likes

b = mapper.of(sorted(c, key=lambda brick: brick[-1].start))
b = b > enumerate
b |= star(lambda idx, x: (idx + 1, x[:-1], x[-1].stop - x[-1].start))
# b is brick iterator
# each brick has an id, the xy slice, and the height

totbricks = len(a)

heightmap = np.zeros(shape, dtype=np.uint32) # height of each xy cell
brickmap = np.zeros(shape, dtype=np.uint16) # top brick of ever cell

supports: dict[int, set[int]] = defaultdict(set) # this brick supports which bricks (x supports?)
ontopof: dict[int, set[int]] = defaultdict(set) # this brick is on top of? (x ontopof?)

for idx, xyslice, height in b:

    maxz = heightmap[xyslice].max()

    # possible landing bricks
    p = brickmap[xyslice]
    if maxz != 0:
        supp = p[heightmap[xyslice] == maxz]
        supp = set(supp)
        ontopof[idx].update(supp)
        # set(supp) is the set of all bricks this brick rests on
        # hence naturally we have the "base closure" (idx -> bricks it rests on)
        # we want the opposite mapping (idx -> bricks resting on this
        consume(map(lambda x: supports[x].add(idx), supp))

        # if len(set(supp)) == 1:
        #     unsafe_br.add(supp[0])

    heightmap[xyslice] = maxz + height
    brickmap[xyslice] = idx

# ontopof and supports are sufficient information to compute the "falling closure"

# The implementation trap here is
# A supports [X, Y, Z, ...]
# X, Y support B
# A supports B
# Y supports C, but F supports C but A does not support F

# step 1, calculate the supporting closure (who are ultimately supported by this brick)
# step 2 shake the tree (who are ONLY supported by this brick?) (easy, we have ontopof)

@cache
def supportswho(idx): # now we know idx supports which all nodes as a set
    acc = {idx,}
    for i in supports[idx]:
        acc |= supportswho(i)
    return acc


# falling closure
def falling(idx):
    resting_on_this = supportswho(idx)
    closure = resting_on_this.copy()
    for i in resting_on_this:
        if i not in closure or i == idx: continue
        if not ontopof[i].issubset(closure): # any nodes from outside? then drop i by shaking
            closure.difference_update(supportswho(i))
    return closure

print(mapper.of(range(1, totbricks + 1)) | falling | len | (lambda x: x-1) >= sum, time() - _n)