
tb = str.maketrans(".#", "01")

# with open("day13/input.txt", "r") as fp:
with open("day13/example.txt", "r") as fp:
    d = map(lambda k: (k != "\n" and k.removesuffix("\n").translate(tb) + ",") or "\n", fp.readlines())

# with open("day13/proc.txt", "w") as fp:
with open("day13/example.txt", "w") as fp:
    fp.writelines(map(str, d))