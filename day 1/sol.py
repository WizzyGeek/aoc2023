
def get_first_dig(l: list[str]):
    for i in l:
        if i.isdigit():
            return i

def get_last_dig(l):
    for i in reversed(l):
        if i.isdigit():
            return i

def get_num(l):
    return int(get_first_dig(l) + get_last_dig(l))

def ans(s):
    return sum(get_num(l) for l in s)

with open("input.txt", "r") as fp:
    print(ans(fp.readlines()))