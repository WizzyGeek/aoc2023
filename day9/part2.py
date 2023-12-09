from itertools import pairwise

def extrapolate(ts):
    if len(ts) == 1:
        return ts[0]
    if any(ts):
        return ts[0] - extrapolate(list(map(lambda k: k[1] - k [0], pairwise(ts))))
    return 0

with open("day9/input.txt", "r") as fp:
    print(sum(map(lambda k: extrapolate(list(map(int, k.split()))), fp.readlines())))