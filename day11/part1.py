import numpy as np
from itertools import combinations, starmap


with open("day11/input.txt", "r") as fp:
    d = np.array(list(map(lambda k: list(k.strip()), fp.readlines())), ndmin=2) == "#"

print(np.where(~np.any(d, axis=1)), np.where(~np.any(d, axis=0)))
d = np.insert(d, np.where(~np.any(d, axis=1))[0], False, axis=0)
d = np.insert(d, np.where(~np.any(d, axis=0))[0], False, axis=1)

idc = np.vstack(np.where(d))

print(sum(starmap(lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1]), combinations(idc.T, 2))))
