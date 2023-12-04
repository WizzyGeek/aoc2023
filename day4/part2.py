
with open("day4/input.txt", "r") as fp:
    d = list(map(lambda j:  (f := len(set(j[0].split()) & set(j[1].split()))), map(lambda k: k.strip().split(":")[1].split("|"), fp.readlines())))

counts = [1 for i in d]

for idx, i in enumerate(d):
    for j in range(1, i + 1):
        try:
            counts[idx + j] += counts[idx]
        except IndexError:
            break
    # print(idx, i, counts)

print(sum(counts))