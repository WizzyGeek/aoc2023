
from itertools import cycle


def parse_line(l):
    a = map(str.strip, l.split("="))
    b = next(a)
    c = map(str.strip, next(a).lstrip("(").rstrip(")").split(","))
    return b, (next(c), next(c))


with open("day8/example.txt", "r") as fp:
    m = cycle(map(lambda i: i == "R", fp.readline().strip()))

    d = dict(map(parse_line, fp.readlines()[1:]))

curr = "AAA"
s = 0
for i in m:
    curr = d[curr][i]
    s += 1
    if curr == "ZZZ":
        break

print(curr, s)