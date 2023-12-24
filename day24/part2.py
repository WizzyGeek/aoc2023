
from itertools import chain, count, islice, tee

from more_itertools import take
from wafle import mapper, rpartial

a = mapper.of(open("day24/input.txt", "r").readlines()) | str.strip | rpartial(str.split, "@") > chain.from_iterable
a |= str.strip
a |= rpartial(str.split, ", ")
a |= (lambda k: tuple(map(int, k)))

b, c = tee(a, 2)
b = islice(b, 0, None, 2)
c = islice(c, 1, None, 2)
a = mapper.of(zip(b, c))

import z3

s = z3.Solver()

sp = z3.Ints("x y z")
sv = z3.Ints("vx vy vz")

t = z3.Ints("t1 t2 t3")
tt = iter(t)
ct = count()
for p, v in take(len(t), a):
    dt = next(tt)
    c = next(ct)
    pxyz = z3.Ints(f"x{c} y{c} z{c}")
    vxyz = z3.Ints(f"vx{c} vy{c} vz{c}")

    for a, vs, x, vx in zip(sp, sv, pxyz, vxyz):
        s.add(a - x + (vs - vx) * dt == 0)

    for i, val in zip(pxyz, p):
        s.add(i == val)

    for i, val in zip(vxyz, v):
        s.add(i == val)

print(s)
print(s.check())

m = s.model()
print("===", m)
print("===", m.eval(z3.Sum(sp)))
