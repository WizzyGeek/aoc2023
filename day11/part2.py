import numpy as np
from itertools import accumulate, combinations, starmap


with open("day11/input.txt", "r") as fp:
    d = np.array(list(map(lambda k: list(k.strip()), fp.readlines())), ndmin=2) == "#"

print(np.where(~np.any(d, axis=1)), np.where(~np.any(d, axis=0)))
# d = np.insert(d, np.where(~np.any(d, axis=1))[0], False, axis=0)
# d = np.insert(d, np.where(~np.any(d, axis=0))[0], False, axis=1)

aa = 1000000 - 1
# aa = 1
colmap = list(starmap(lambda k, i: k + i, zip(accumulate(map(lambda a: a * aa, ~np.any(d, axis=0))), range(d.shape[1]))))
rowmap = list(starmap(lambda k, i: k + i, zip(accumulate(map(lambda a: a * aa, ~np.any(d, axis=1))), range(d.shape[0]))))
print(colmap, rowmap)
idc = np.vstack(np.where(d))

print(sum(starmap(lambda a, b: abs(rowmap[a[0]] - rowmap[b[0]]) + abs(colmap[a[1]] - colmap[b[1]]), combinations(idc.T, 2))))
