
from collections import defaultdict
from functools import cache, partial
import pprint
from wafle import mapper
import sys
import operator as op

sys.setrecursionlimit(141 * 141)

m = mapper.of(open("day23/input.txt", "r").readlines()) | str.strip | list >= list

d = {complex(r, c): ch for (r, citr) in (mapper.of(m) | enumerate > enumerate) for c, ch in citr}

vec = [1j, -1j, 1, -1]

end = max(d, key=abs)
tgt = end - 1j

def iter_len(itr) -> tuple[bool, complex | None]:
    try:
        a = next(itr)
    except StopIteration:
        return False, None

    try:
        next(itr)
    except StopIteration:
        return True, a
    else:
        return False, None

@cache
def portal(f: complex, last: complex) -> tuple[complex, int, complex]:
    s = {last,}
    l, v = iter_len(filter(lambda p: p not in s and p in d and d[p] != "#", map(partial(op.add, f), vec)))
    lf = last
    while l:
        s.add(f)
        lf = f
        f = v
        l, v = iter_len(filter(lambda p: p not in s and p in d and d[p] != "#", map(partial(op.add, f), vec)))
    s.remove(last)
    return f, len(s) + (lf != last), lf

# print(portal(1+1j, 1j))

adj_mat: dict[complex, dict[complex, int]] = defaultdict(dict)
discovered = set()
to_add: list[tuple[complex, complex]] = [] # first node, second is child which should be excluded

to_add.append((1j, 0j))

while to_add:
    curr, par = to_add.pop()
    if curr in discovered: continue
    for child in filter(lambda p: p != par and p in d and d[p] != "#", map(lambda x: curr + x, vec)):
        dest, weight, dpar = portal(child, curr)
        adj_mat[curr][dest] = weight
        adj_mat[dest][curr] = weight
        to_add.append((dest, dpar))
        discovered.add(curr)

pprint.pprint(adj_mat)
# Now we have an adjcency matrix type thingy

ma = -1
def longest_path(f: complex, path: frozenset, dist: int):
    if f == tgt:
        global ma
        ma = max(ma, dist)
        return

    for node, weight in adj_mat[f].items():
        if node not in path:
            longest_path(node, path | {node,}, dist + weight)

longest_path(1j, frozenset([1j,]), 0)
print(ma)