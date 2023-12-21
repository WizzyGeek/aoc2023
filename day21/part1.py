
from __future__ import annotations

from collections import deque
from itertools import chain
from more_itertools import consume
from wafle import mapper, star

a = mapper.of(open("day21/example.txt", "r").readlines()) | str.strip | enumerate > enumerate

d = {}
pos = 0
for r, l in a:
    for c, ch in l:
        d[r + c * 1j] = ch
        if ch == "S":
            pos = r + c * 1j

# print(d, pos)
end = max(d, key=abs)

def steps_pos(step, cur):
    step += 1
    l, r, u, do = cur - 1j, cur + 1j, cur - 1, cur + 1
    if l in d and d[l] != "#": yield step, l
    if r in d and d[r] != "#": yield step, r
    if u in d and d[u] != "#": yield step, u
    if do in d and d[do] != "#": yield step, do

q = deque()
vis = set()

def s_vis(k):
    if k in vis: return
    q.append(k)
    vis.add(k)

s_vis((0, pos))

def one_step(q: deque):
    vis.clear() # limit memory
    (mapper.of(range(len(q))) | (lambda x: q.popleft()) | star(steps_pos) > chain.from_iterable) | s_vis >= consume


mapper.of(range(5)) | (lambda x: q) | one_step >= consume

print(len(set(q)))
# print(set(q))