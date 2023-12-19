
from functools import partial
from itertools import dropwhile, filterfalse, groupby
from wafle import mapper, rpartial
import operator as op

a = mapper.of(open("day19/input.txt", "r").readlines()) > rpartial(groupby, str.isspace)
a = a | rpartial(op.getitem, 1) | list
a = a > partial(filterfalse, lambda x: x[0].isspace())
wf, items = a | mapper.of

Item = tuple[int, int, int, int]

imap = {"x": 0, "m": 1, "a": 2, "s": 3}
opmap = {
    ">": op.gt,
    "<": op.lt
}

def make_condition(rule: str):
    cond, ns = rule.split(":")
    param, opr, val = imap[cond[0]], opmap[cond[1]], int(cond[2:])
    def applies(item: Item):
        return (None, ns)[opr(item[param], val)]
    return applies

def parse_rule(l: list[str]):
    rules, state = l[:-1], l[-1]
    def applies_regardless(item: Item):
        return state
    calls = tuple(map(make_condition, rules)) + (applies_regardless,)
    def next_state(item: Item):
        for app in calls:
            ret = app(item)
            if ret is not None:
                return ret
        raise Exception("failed")
    return next_state

wf = wf | rpartial(op.getitem, slice(-2)) | rpartial(str.split, "{") | (lambda x: (x[0], parse_rule(x[1].split(",")))) >= dict

start = wf["in"]

items = items | str.strip | rpartial(op.getitem, slice(1, -1)) | rpartial(str.split, ",") | (lambda x: ("in", tuple(map(lambda k: int(k.split("=")[1]), x)))) >= list

g = 0
def one_cycle(items):
    global g
    nw = []
    for state, i in items:
        ns = wf[state](i)

        if ns == "A":
            g += sum(i)
            continue
        elif ns == "R":
            continue
        nw.append((ns, i))
    return nw

while items:
    items = one_cycle(items)

print(g)