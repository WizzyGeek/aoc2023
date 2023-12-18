from functools import partial
from itertools import pairwise, product
from more_itertools import consume
import numpy as np
from wafle import mapper, star, rpartial
import sys
import operator as op

dmap = {
    "U": -1+0j,
    "D": 1+0j,
    "R": 1j,
    "L": -1j
}

dl = [1j, 1+0j, -1j, -1+0j]

a = mapper.of(open("day18/input.txt", "r").readlines()) | str.strip | str.split | rpartial(op.getitem, 2) | rpartial(op.getitem, slice(2, -1)) | (lambda k: dl[int(k[-1])] * int(k[:-1], 16))

pos = 0 + 0j
mr, mi = 0.0, 0.0
mmr, mmi = 0.0, 0.0
v = [(0, 0)]
g = 0
for dir in a:
    pos += dir
    g += abs(dir)
    v.append((int(pos.real), int(pos.imag)))
    mr, mi = max(pos.real, mr), max(pos.imag, mi)
    mmr, mmi = min(pos.real, mmr), min(pos.imag, mmi)

mr = int(mr + 1 - mmr)
mi = int(mi + 1 - mmi)

v2 = mapper.of(v) | star(lambda y, x: (int(y - mmr), int(x - mmi))) > pairwise
v2 |= star(lambda f, s: f[1] * s[0] - s[1] * f[0])
s = v2 >= sum
print(int(s / 2 + g / 2 + 1))


