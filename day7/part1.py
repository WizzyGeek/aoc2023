from collections import Counter

strmap = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2
}

trans = str.maketrans("TJQKA", "ABCDE")

def parse_hand(a):
    b = Counter(a)
    return list(map(lambda k: k[1], b.most_common())), a.translate(trans)

def parse_line(l):
    g = l.split()
    p = parse_hand(g[0])
    return p[0], p[1], int(g[1])

with open("day7/input.txt", "r") as fp:
    d = list(map(parse_line,fp.readlines()))

d.sort()
print(d, len(d))
s = 0
for idx, i in enumerate(d, 1):
    s += i[2] * idx

print(s)