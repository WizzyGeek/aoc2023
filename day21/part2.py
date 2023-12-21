
from __future__ import annotations

from collections import deque
from functools import partial
from itertools import chain
from more_itertools import consume
from wafle import mapper, star

a = mapper.of(open("day21/input.txt", "r").readlines()) | str.strip | enumerate > enumerate

d = {}
pos = 0
for r, l in a:
    for c, ch in l:
        d[r + c * 1j] = ch
        if ch == "S":
            pos = r + c * 1j

# print(d, pos)
end = max(d, key=abs) + 1 + 1j

def wrap(c: complex):
    return complex(c.real % end.real, c.imag % end.imag)

# def steps_pos(cur):
#     l, r, u, do = cur - 1j, cur + 1j, cur - 1, cur + 1
#     if l in d and d[l] != "#": yield l
#     if r in d and d[r] != "#": yield r
#     if u in d and d[u] != "#": yield u
#     if do in d and d[do] != "#": yield do

def steps_pos(cur):
    orig = (cur - 1j, cur + 1j, cur - 1, cur + 1)
    l, r, u, do = map(wrap, orig)
    if d[l] != "#": yield orig[0]
    if d[r] != "#": yield orig[1]
    if d[u] != "#": yield orig[2]
    if d[do] != "#": yield orig[3]

def get_vistable(n, needed):
    q = deque()
    vis = set()

    def s_vis(k):
        if k in vis: return
        q.append(k)
        vis.add(k)

    s_vis(pos)

    def one_step(q: deque):
        vis.clear() # limit memory
        (mapper.of(range(len(q))) | (lambda x: q.popleft()) | steps_pos > chain.from_iterable) | s_vis >= consume


    for step, _ in (mapper.of(range(n)) | (lambda x: q) | one_step >= partial(enumerate, start=1)):
        if step in needed:
            yield step, len(vis)

with open("day21/points.txt", "w") as fp:
    for i in get_vistable(1000, range(65, 1000, 131)):
        print(i[0], i[1], file=fp)
        print(i)

# for i in get_vistable(1000, {6, 10, 50, 100, 500, 1000}):
#         # print(i[0], i[1], file=fp)
#         print(i)

# print(set(q))
