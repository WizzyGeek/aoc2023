import math

with open("day4/input.txt", "r") as fp:
    d = sum(map(lambda j:  (2 ** (f := (len(set(j[0].split()) & set(j[1].split())) - 1))) * bool(f + 1), map(lambda k: k.strip().split(":")[1].split("|"), fp.readlines())))

print(d)