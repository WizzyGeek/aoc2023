from dataclasses import dataclass
from functools import partial, reduce
from itertools import filterfalse, groupby
from wafle import mapper, rpartial
import operator as op

a = mapper.of(open("day19/input.txt", "r").readlines()) > rpartial(groupby, str.isspace)
a = a | rpartial(op.getitem, 1) | list
a = a > partial(filterfalse, lambda x: x[0].isspace())
wf, items = a | mapper.of

Item = tuple[int, int, int, int]

imap = {"x": 0, "m": 1, "a": 2, "s": 3}

LOWER = 1
UPPER = 4001

class Interval:
    @classmethod
    def f(cls, start, end):
        return cls(start, end - start)

    def __init__(self, start, len):
        self.start = start
        self.len = len
        self.end = start + len

    def __len__(self):
        return max(self.len, 0)

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
        if not other:
            return self
        if other.end == self.end:
            return Interval.f(self.start, other.start)
        if self.start == other.start:
            return Interval.f(other.end, self.end)
        else:
            raise Exception("fuck")
            return (Interval.f(self.start, other.start), Interval.f(other.end, self.end))

    def __repr__(self):
        return f"({self.start}, {self.end})"

def make_condition(rule: str):
    cond, ns = rule.split(":")
    param, opr, val = imap[cond[0]], cond[1], int(cond[2:])

    if opr == ">":
        intr = Interval.f(val + 1, UPPER)
    else: # <
        intr = Interval.f(LOWER, val)
    return param, intr, ns

def parse_rule(l: list[str]):
    rules, state = l[:-1], l[-1]
    calls = tuple(map(make_condition, rules)) + ((0, Interval.f(LOWER, UPPER), state),)
    return calls

wf = wf | rpartial(op.getitem, slice(-2)) | rpartial(str.split, "{") | (lambda x: (x[0], parse_rule(x[1].split(",")))) >= dict
# items = items | str.strip | rpartial(op.getitem, slice(1, -1)) | rpartial(str.split, ",") | (lambda x: ("in", tuple(map(lambda k: int(k.split("=")[1]), x)))) >= list

print(wf)

class Tetra:
    d: list[Interval]

    def __init__(self, d = None) -> None:
        self.d = d or [Interval.f(LOWER, UPPER), Interval.f(LOWER, UPPER), Interval.f(LOWER, UPPER), Interval.f(LOWER, UPPER)]

    def do_op(self, param, ointr):
        overlap = self.d[param] & ointr
        leftover = self.d[param] - overlap
        # print(leftover, overlap, self.d[param])

        self.d[param] = overlap
        yield self

        d = self.d.copy()
        d[param] = leftover
        yield Tetra(d)

    def __bool__(self):
        return all(self.d)

    def __repr__(self) -> str:
        return str(self.d)

    def __len__(self) -> int:
        return reduce(op.mul, map(len, self.d))

acc = []

def follow_rule(rec: Tetra, rule: tuple[tuple[int, Interval, str], ...]):
    proc = [rec]
    procd = []
    for p, oi, ns in rule:
        nproc = []
        for i in proc:
            ts, nr = tuple(i.do_op(p, oi))
            if ts:
                if ns == "A":
                    acc.append(ts)
                elif ns != "R":
                    procd.append((ts, ns))
            if nr:
                nproc.append(nr)
        proc = nproc
    if proc: print("AAAAAAAAA", proc)
    return procd

q = [(Tetra(), "in")]
while q:
    cs = q.pop()
    q.extend(follow_rule(cs[0], wf[cs[1]]))

# print(q, acc)
print(sum(map(len, acc)))