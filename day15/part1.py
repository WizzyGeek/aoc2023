
from functools import reduce


def HASH(x):
    return reduce(lambda a, b: ((a + b) * 17) % 256, map(ord, x), 0)

with open("day15/input.txt", "r") as fp:
    d = sum(map(HASH, fp.read().strip().split(",")))

print(d)