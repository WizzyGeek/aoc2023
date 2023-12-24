
from itertools import chain, combinations, islice, tee

from wafle import mapper, rpartial, star
import numpy as np

a = mapper.of(open("day24/input.txt", "r").readlines()) | str.strip | rpartial(str.split, "@") > chain.from_iterable
a |= str.strip
a |= rpartial(str.split, ", ")
a |= (lambda k: tuple(map(int, k))[:-1]) # drop z

b, c = tee(a, 2)
b = islice(b, 0, None, 2)
c = islice(c, 1, None, 2)
a = mapper.of(zip(b, c))

a |= star(lambda xy, vxy: ((-1 * vxy[1], vxy[0]), vxy[0] * xy[1] - vxy[1] * xy[0], xy, vxy))
a = a > rpartial(combinations, 2)
a |= star(lambda f, s: ((f[0], s[0]), (f[1], s[1]), np.array((f[2], s[2])), np.array((f[3], s[3]))))

LOWER = 2e14
UPPER = 4e14

# LOWER = 7
# UPPER = 27

@star
def solve(A, b, offsets, velocities):
    try:
        # print(A, b)
        xy = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        Ab = np.hstack((A, ((b[0],), (b[1],))))
        if np.linalg.det(Ab[:, ::2]) == 0 and np.linalg.det(Ab[:, 1::1]):
            print("AAAAAAA BAD THINGS") # We are fucked
            return True
        return False
    else:
        dx, dy = min(abs(xy[0] - LOWER), abs(xy[0] - UPPER)), min(abs(xy[1] - LOWER), abs(xy[1] - UPPER))
        if dx <= 1 or dy <= 1: print("EDGE VALUES: ", dx, dy, A, xy, b)

        if all(LOWER <= i <= UPPER for i in xy):
            t1 = (xy - offsets[0]) / velocities[0]
            t2 = (xy - offsets[1]) / velocities[1]
            if t2[0] == 0 or t1[0] == 0: print("EDGE CASE")
            if t1[0] > 0 and t2[0] > 0:
                return True
            return False
        return False

a |= solve

print(a >= sum)

#  > rpartial(combinations, 2)

