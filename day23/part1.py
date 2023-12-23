
from functools import cache, partial
from wafle import mapper
import sys
import operator as op

sys.setrecursionlimit(141 * 141)

m = mapper.of(open("day23/input.txt", "r").readlines()) | str.strip | list >= list

d = {complex(r, c): ch for (r, citr) in (mapper.of(m) | enumerate > enumerate) for c, ch in citr}

vec = [1j, -1j, 1, -1]

vmap = { # map of character to required velocity
    ">": 1j,
    "<": -1j,
    "v": 1,
}

end = max(d, key=abs)
tgt = end - 1j

@cache
def longest_path(f: complex, vis: frozenset[complex]):
    if f == tgt:
        return 0

    vis |= {f,}
    ma = -1
    for pos in filter(lambda p: p not in vis and p in d and d[p] != "#", map(partial(op.add, f), vec)):
        if d[pos] in vmap and vmap[d[pos]] != (pos - f): continue
        g = longest_path(pos, vis)
        if g > ma:
            ma = g
    if ma == -1:
        return -141 * 141 # invalidate branch
    return ma + 1

print(longest_path(1j, frozenset()))

