
import numpy as np
from itertools import chain
from wafle import mapper, rpartial

a = ((mapper.of(open("day21/points.txt", "r").readlines()) | str.strip | str.split > chain.from_iterable) | int) >= list
x, y = a[::2], a[1::2]
print(x, y)

_x = x
x = [0, 1, 2]

# 202300 * 131 + 65

# print(mapper.of(x) | (lambda x: [1, x, x * x]) >= list)
# b = np.linalg.inv(mapper.of(x) | (lambda x: [1, x, x * x]) >= list) @ np.array(y).reshape((3, 1))
# print(b) # Why do this to me god

d = 26501365 // 131
print(d)
b = np.linalg.inv(mapper.of(x) | (lambda x: [1, x, x * x]) >= list) @ np.array(y).reshape((3, 1))
c2 = np.array(b * 2, np.uint64)
print(int(c2[2] * d * d + c2[1] * d + c2[0]) // 2)