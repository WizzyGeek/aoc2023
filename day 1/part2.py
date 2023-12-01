d = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

def get_first_dig(l: str):
    for idx, i in enumerate(l):
        if i.isdigit():
            return i
        if l[idx:idx+3] in d or l[idx:idx + 4] in d or l[idx:idx+5] in d:
            return d.get(l[idx:idx+3]) or d.get(l[idx:idx+4]) or d.get(l[idx:idx+5])

def get_last_dig(l):
    for idx, i in reversed(list(enumerate(l))):
        if i.isdigit():
            return i
        if l[idx-2:idx+1] in d or l[idx-3:idx+1] in d or l[idx-4:idx+1] in d:
            return d.get(l[idx-2:idx+1]) or d.get(l[idx-3:idx+1]) or d.get(l[idx-4:idx+1])


def get_num(l):
    return int(get_first_dig(l) + get_last_dig(l))

def ans(s):
    return sum(get_num(l) for l in s)

with open("input.txt", "r") as fp:
    print(ans(fp.readlines()))