
from collections import defaultdict


with open("day3/input.txt", "r") as fp:
    d = list(map(str.strip, fp.readlines()))

lc = len(d[0])
l = len(d)

cm: dict[tuple[int, int], list] = defaultdict(list)

in_bounds = lambda j: j[1] >= 0 and j[0] >= 0 and j[1] < lc and j[0] < l

def boundary(y, x):
    return [(y, x - 1), (y, x + 1), (y + 1, x), (y + 1, x - 1), (y + 1, x + 1), (y - 1, x), (y - 1, x + 1), (y - 1, x - 1)]

acc = ""
to_add = False
to_app: set[tuple[int, int]] = set()
for rx, r in enumerate(d):
    for cx, c in enumerate(r):
        if not c.isdigit():
            if acc != "":
                g = int(acc)
                for t in to_app:
                    cm[t].append(g)
                to_app.clear()
                acc = ""
        else:
            acc += c
            to_app.update(list(filter(lambda k: d[k[0]][k[1]] == "*", filter(in_bounds, boundary(rx, cx)))))

    if acc != "":
        g = int(acc)
        for t in to_app:
            cm[t].append(g)
        to_app.clear()
        acc = ""

print(sum(map(lambda p: p[0] * p[1], filter(lambda k: len(k) == 2, cm.values()))))