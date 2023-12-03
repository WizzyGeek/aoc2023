
with open("day3/input.txt", "r") as fp:
    d = list(map(str.strip, fp.readlines()))

lc = len(d[0])
l = len(d)
in_bounds = lambda j: j[1] >= 0 and j[0] >= 0 and j[1] < lc and j[0] < l

def boundary(y, x):
    return [(y, x - 1), (y, x + 1), (y + 1, x), (y + 1, x - 1), (y + 1, x + 1), (y - 1, x), (y - 1, x + 1), (y - 1, x - 1)]

acc = ""
to_add = False
s = 0
for rx, r in enumerate(d):
    for cx, c in enumerate(r):
        if not c.isdigit():
            if acc != "":
                if to_add:
                    s += int(acc)
                    to_add = False
                acc = ""
        else:
            acc += c
            to_add = to_add or any(map(lambda k: (not (f := d[k[0]][k[1]]).isdigit()) and f != ".", filter(in_bounds, boundary(rx, cx))))

    if acc != "":
        if to_add:
            s += int(acc)
            to_add = False
        acc = ""

print(s)