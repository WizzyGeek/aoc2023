
from collections import deque, namedtuple
from dataclasses import dataclass, field
from functools import cache, partial
from queue import PriorityQueue
from more_itertools import consume
from wafle import mapper
import sys
import operator as op

sys.setrecursionlimit(141 * 141)

m = mapper.of(open("day23/input.txt", "r").readlines()) | str.strip | list >= list

d = {complex(r, c): ch for (r, citr) in (mapper.of(m) | enumerate > enumerate) for c, ch in citr}

vec = [1j, -1j, 1, -1]

# vmap = { # map of character to required velocity
#     ">": 1j,
#     "<": -1j,
#     "v": 1,
# }

end = max(d, key=abs)
tgt = end - 1j

# Optimisation 1: Um IDK

# @dataclass(order=True, slots=True)
# class Node:
#     cost: int = field(compare=True)
#     pos: complex = field(compare=False)
#     path: frozenset = field(compare=False)

#     def __iter__(self):
#         yield self.cost
#         yield self.pos
#         yield self.path

# q: PriorityQueue[Node] = PriorityQueue()
# costs = {}

# q.put_nowait(Node(0, 1j, frozenset()))
# push = q.put_nowait
# pop = q.get_nowait

# while not q.empty():
#     cost, f, vis = pop()
#     vis |= {f,}
#     consume(map(push, filter(lambda p: p.pos not in vis and p.pos in d and d[p.pos] != "#", map(lambda k: Node(cost - 1, f + k, vis), vec))))
#     costs[f] = max(abs(cost), costs.get(f, 0))
#     if f == tgt:
#         print(costs[tgt])

# print(costs[tgt])

# base solve

# def iter_len(itr):
#     try:
#         a = next(itr)
#     except StopIteration:
#         return False, None

#     try:
#         next(itr)
#     except StopIteration:
#         return True, a
#     else:
#         return False, None

# portals: dict[complex, tuple[complex, set]] = {}
# ns = frozenset()

# @cache
# def longest_path(f: complex, vis: frozenset[complex]):
#     if f == tgt:
#         return 0

#     vis |= {f,}
#     ma = -1
#     for pos in filter(lambda p: p not in vis and p in d and d[p] != "#", map(partial(op.add, f), vec)):
#         # if d[pos] in vmap and vmap[d[pos]] != (pos - f): continue

#         dest = pos, ns
#         if pos not in portals:
#             # print(1)
#             o = pos
#             s = {pos,}
#             l, v = iter_len(filter(lambda p: p != f and p not in s and p in d and d[p] != "#", map(partial(op.add, pos), vec)))
#             while l:
#                 s.add(pos)
#                 pos = v
#                 l, v = iter_len(filter(lambda p: p not in s and p in d and d[p] != "#", map(partial(op.add, pos), vec)))
#             portals[o] = (pos, s)
#             pos = o
#             # portals[pos] = (o, s)
#         dest = portals[pos]

#         g = longest_path(dest[0], vis | dest[1]) + len(dest[1])
#         if g > ma:
#             ma = g
#     if ma == -1:
#         return -141 * 141 # invalidate branch
#     return ma + 1

# # print(longest_path(1j, frozenset()))
# try:
#     print(longest_path(1j, frozenset()))
# except:
#     print(portals)
# else:
#     print(portals)

# Optimisation 2: DFS BFS

# meth = ""
# q = deque()
# State = namedtuple("State", ["path", "at"])
# ma = 0

# push = q.append
# pop = q.popleft if meth == "BFS" else q.pop

# push(State(frozenset(), 1j))

# while q:
#     s = pop()
#     if s.at == tgt: ma = max(ma, len(s.path))
#     else:
#         vis = s.path | {s.at,}
#         q.extend(map(partial(State, vis), filter(lambda p: p not in vis and p in d and d[p] != "#", map(partial(op.add, s.at), vec))))

# print(ma)
