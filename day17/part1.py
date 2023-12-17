from __future__ import annotations

from queue import PriorityQueue
from dataclasses import dataclass, field

with open("day17/input.txt", "r") as fp:
    d = { complex(row, col): h for (row, rowitr) in enumerate(map(lambda k: enumerate(map(int, k.strip())), fp.readlines())) for col, h in rowitr }

ld = max(d, key=abs)

print(ld)
pq: PriorityQueue[State] = PriorityQueue()

@dataclass(frozen=True, slots=True, order=True, eq=True)
class State:
    heat_loss: int
    curr: complex = field(compare=False)
    velocity: complex = field(compare=False)
    moves: int = field(compare=False)

    def identitiy(self):
        return self.curr, self.velocity, self.moves

# Need (heat_loss, curr, velocity, moves)

pq.put(State(0, 0j, 1j, 1))
pq.put(State(0, 0j, 1, 1))

visited = set()
while not pq.empty():
    s = pq.get()
    if (f := s.identitiy()) in visited: continue
    visited.add(f)

    if s.curr == ld:
        print(s.heat_loss)
        break

    if s.moves < 3:
        ne = s.curr + s.velocity
        ne in d and pq.put(State(d[ne] + s.heat_loss, ne, s.velocity, s.moves + 1))
    ne = s.curr + (1j * s.velocity)
    ne in d and pq.put(State(d[ne] + s.heat_loss, ne, s.velocity * 1j, 1))
    ne = s.curr - (1j * s.velocity)
    ne in d and pq.put(State(d[ne] + s.heat_loss, ne, s.velocity * -1j, 1))
