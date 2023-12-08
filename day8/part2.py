
from itertools import cycle
from math import lcm


def parse_line(l):
    a = map(str.strip, l.split("="))
    b = next(a)
    c = map(str.strip, next(a).lstrip("(").rstrip(")").split(","))
    return b, (next(c), next(c))


with open("day8/example.txt", "r") as fp:
    m = list(map(lambda i: i == "R", fp.readline().strip()))

    d = dict(map(parse_line, fp.readlines()[1:]))

curr = list(filter(lambda k: k.endswith("A"), d))

def get_loop(cur, moves):
    s = 0
    for i in cycle(moves):
        cur = d[cur][i]
        s += 1
        if cur.endswith("Z"):
            break
    return s

print(lcm(*(get_loop(j, m) for j in curr)))
# s = 0
# print(curr)
# for i in m:
#     curr = list(d[j][i] for j in curr)
#     s += 1
#     if all(j.endswith("Z") for j in curr):
#         break

# print(curr, s)