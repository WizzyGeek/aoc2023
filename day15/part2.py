
from functools import reduce


def HASH(x):
    return reduce(lambda a, b: ((a + b) * 17) % 256, map(ord, x), 0)

def do_op(x, tab: list[list[tuple[str, int]]]):
    if x[-1] == "-":
        k = x[:-1]
        b = HASH(k)
        for idx, i in enumerate(tab[b]):
            if i[0] == k:
                tab[b].pop(idx)
                return
        # raise Exception("1")
    elif x[-2] == "=":
        v = int(x[-1])
        k = x[:-2]
        b = HASH(k)
        for idx, i in enumerate(tab[b]):
            if i[0] == k:
                tab[b][idx] = k, v
                return
        tab[b].append((k, v))
    else:
        raise Exception()

with open("day15/input.txt", "r") as fp:
    d = fp.read().strip().split(",")

tab: list[list[tuple[str, int]]] = [list() for i in range(256)]

for i in d:
    do_op(i, tab)

s = 0
for boxv, box in enumerate(tab, 1):
    for slot, rec in enumerate(box, 1):
        s += boxv * slot * rec[1]

print(s, tab)