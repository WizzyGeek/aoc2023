
with open("day5/input.txt", "r") as fp:
    d = fp.readlines()

seeds = {i: i for i in map(int, d[0].split(":")[1].split())}

def parse_map(lines, pmap:dict):
    r = {}
    for i in lines:
        dest, source, len = tuple(map(int, i.split()))
        to_del = []
        for k, v in pmap.items():
            if v >= source and v < source + len:
                r[k] = v - source + dest
                to_del.append(k)
        for i in to_del: del pmap[i]
    r.update(pmap)
    return r

c = d.index("seed-to-soil map:\n", 0)
l = d.index("\n", c+1)
seeds = parse_map(d[c+1:l], seeds)

c = d.index("soil-to-fertilizer map:\n", l)
l = d.index("\n", c+1)
seeds = parse_map(d[c+1:l], seeds)

c = d.index("fertilizer-to-water map:\n", l)
l = d.index("\n", c+1)
seeds = parse_map(d[c+1:l], seeds)

c = d.index("water-to-light map:\n", l)
l = d.index("\n", c+1)
seeds = parse_map(d[c+1:l], seeds)

c = d.index("light-to-temperature map:\n", l)
l = d.index("\n", c+1)
seeds = parse_map(d[c+1:l], seeds)

c = d.index("temperature-to-humidity map:\n", l)
l = d.index("\n", c+1)
seeds = parse_map(d[c+1:l], seeds)

c = d.index("humidity-to-location map:\n", l)
seeds = parse_map(d[c+1:], seeds)

print(min(seeds.values()))