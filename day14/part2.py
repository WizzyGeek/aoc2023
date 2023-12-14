import numpy as np
import sys

sys.set_int_max_str_digits(10000)

tb = str.maketrans(".O#", "\0\1\2")

with open("day14/input.txt", "r") as fp:
    d = np.vstack(tuple(map(lambda k: np.fromstring(k.strip().translate(tb), dtype=np.uint8), fp.readlines())))


d = np.vstack(([2] * d.shape[1], d, [2] * d.shape[1]))
h = np.array([2] * d.shape[0], dtype=np.int32).reshape((-1, 1))

d = np.hstack((h, d, h))
d = np.array(d, np.int32)

def calc_load(d):
    acc: np.ndarray = np.zeros_like(d[0])

    for i, idx in zip(reversed(d), reversed(range(d.shape[0]))):
        n = d.shape[0] - idx - 1
        # print(n, idx)
        acc += (i == 1) * n

    return acc.sum()


# 0 is none
# 1 is rolling
# 2 is cube rock
# Tilt this north, for any rock dont
# assign number but, assign the slice of rolling as 1
def tilt_north(d):
    acc: np.ndarray = np.zeros_like(d[0])

    for i, idx in zip(reversed(d), reversed(range(d.shape[0]))):
        acc += (i == 1)
        for j in np.where((i == 2))[0]:
            d[idx+1:idx+1+acc[j], j] = 1
        d[idx], acc = (i == 2) * d[idx], acc * (i != 2)

    return d

def cycle(d):
    d = tilt_north(d)
    h = tilt_north(np.rot90(d, k = 3))
    h = tilt_north(np.rot90(d, k = 2))
    h = tilt_north(np.rot90(d, k = 1))
    return d

def int_pack(d):
    s = ""
    for i in d[1:-1]:
        for j in i[1:-1]:
            s = str(j) + s
    return int(s, 3)

ip = int_pack
k = {}
itr: list[int] = []

n = 1000000000
for i in range(n):
    cycle(d)
    r = ip(d)
    if r in k:
        start = k[r]
        l = i - start # this is the length
        pred = start + (n - 1 - start) % l
        m = itr[pred]
        break

    k[r] = i # rth board seen after i+1 cycles
    itr.append(r)

def unpack(d, m):
    for i in range(1, d.shape[0] - 1):
        for j in range(1, d.shape[1] - 1):
            m, d[i][j] = divmod(m, 3)

    return d

print(unpack(d, m))
print(calc_load(d))


# k = {}
# for i in range(1000):
#     cycle(d)
#     m = calc_load(d.copy())
#     if m in k:
#         print(i, k[m])
#     k[m] = i

# print(calc_load(d), k)