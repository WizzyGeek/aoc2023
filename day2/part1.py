from itertools import chain
from collections import defaultdict

with open("input.txt", "r") as fp:
    d = fp.readlines()

def p(s: str):
    f = s.strip().split()
    return int(f[0]), f[1]

rgb = (12, 13, 14)
m = 0
for dx, s in enumerate(d, 1):
    t = s.split(":")[1]
    f = map(p, chain.from_iterable(map(lambda k: k.split(","), t.split(";"))))
    j: dict[str, int] = defaultdict(lambda: 0)
    for n, k in f:
        j[k] = max(j[k], n)

    if j["red"] <= rgb[0] and j["blue"] <= rgb[2] and j["green"] <= rgb[1]:
        m += dx

print(m)