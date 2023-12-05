from itertools import pairwise, starmap, groupby

class Interval:
    @classmethod
    def f(cls, start, end):
        return cls(start, end - start)

    def __init__(self, start, len):
        self.start = start
        self.len = len
        self.end = start + len

    def __bool__(self):
        return self.len > 0 # qc

    def __and__(self, other): #qc
        # No overlap
        if self.start >= other.end or other.start >= self.end:
            return None
        return Interval.f(max(self.start, other.start), min(self.end, other.end))

    def map(self, src, to): #qc
        ret = self & src
        if not ret:
            return None
        k = ret.start - src.start
        return Interval(to + k, ret.len)

    def __sub__(self, other): # only for intervals inside it, asymmetric diff
        if other.end == self.end:
            return Interval.f(self.start, other.start)
        if self.start == other.start:
            return Interval.f(other.end, self.end)
        else:
            return (Interval.f(self.start, other.start), Interval.f(other.end, self.end))

    def __repr__(self):
        return f"({self.start}, {self.end})"


with open("day5/input.txt", "r") as fp:
    d = fp.readlines()

def grouper(iterable, n, *, incomplete='strict', fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == 'strict':
        return zip(*args, strict=True)
    if incomplete == 'ignore':
        return zip(*args)
    else:
        raise ValueError('Expected fill, strict, or ignore')

seeds = list(starmap(Interval, grouper(map(int, d[0].split(":")[1].split()), 2)))

def parse_map(lines, pmap: list[Interval]):
    r = []
    for i in lines:
        dest, source, len = tuple(map(int, i.split()))
        src = Interval(source, len)
        for idx, j in enumerate(pmap):
            k = j.map(src, dest)
            if k:
                # complement
                compl = j - (j & src)
                if isinstance(compl, tuple):
                    pmap.append(compl[1])
                    compl = compl[0]
                pmap[idx] = compl
                r.append(k)
                # print(src, pmap[idx], j, j & src, k, dest)

    r.extend(filter(bool, pmap))
    return r


# print(seeds)
c = d.index("seed-to-soil map:\n", 0)
l = d.index("\n", c+1)
seeds = parse_map(d[c+1:l], seeds)
# print(seeds)

c = d.index("soil-to-fertilizer map:\n", l)
l = d.index("\n", c+1)
seeds = parse_map(d[c+1:l], seeds)

# print(seeds)

c = d.index("fertilizer-to-water map:\n", l)
l = d.index("\n", c+1)
seeds = parse_map(d[c+1:l], seeds)

# print(seeds)

c = d.index("water-to-light map:\n", l)
l = d.index("\n", c+1)
seeds = parse_map(d[c+1:l], seeds)

# print(seeds)

c = d.index("light-to-temperature map:\n", l)
l = d.index("\n", c+1)
seeds = parse_map(d[c+1:l], seeds)

# print(seeds)

c = d.index("temperature-to-humidity map:\n", l)
l = d.index("\n", c+1)
seeds = parse_map(d[c+1:l], seeds)

# print(seeds)

c = d.index("humidity-to-location map:\n", l)
seeds = parse_map(d[c+1:], seeds)

# print(seeds)

print(min(map(lambda k: k.start, seeds)))