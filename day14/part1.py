import numpy as np

tb = str.maketrans(".O#", "\0\1\2")

with open("day14/input.txt", "r") as fp:
    d = np.vstack(tuple(map(lambda k: np.fromstring(k.strip().translate(tb), dtype=np.uint8), fp.readlines())))


d = np.vstack((np.array([2] * d.shape[1], dtype=np.uint8), d))
d = np.array(d, np.int32)

acc: np.ndarray = np.zeros_like(d[0])
load = np.zeros_like(d[0], dtype=np.int32)

for i, idx in zip(reversed(d), reversed(range(d.shape[0]))):
    acc += (i == 1)
    d[idx], acc = (i == 2) * (acc), acc * (i != 2)
    n = d.shape[0] - idx - 1
    # print((n * (n + 1)) // 2 - ((n - d[idx]) * (n - d[idx] + 1)) // 2, d[idx], n)
    load += (n * (n + 1)) // 2 - ((n - d[idx]) * (n - d[idx] + 1)) // 2

print(load.sum())