# False is low
# True is high
from __future__ import annotations
from collections import deque, namedtuple
from functools import partial
import operator as op
from more_itertools import consume

from wafle import star, mapper


# Pulses need following info
# Who is sending? -> Str
# What is sent? -> Bool

Pulse = namedtuple("Pulse", ["t", "i"])

sym = ("-low->", "-high->")
def printp(pulse, mod):
    print(pulse.i.name, sym[pulse.t], mod.name)

# c = [0, 0]
# broadcaster
class Module:
    observors: list[Module]

    def  __init__(self, name) -> None:
        self.name = name
        self.observors = []
        T = Pulse(True, self)
        F = Pulse(False, self)
        self.P = (F, T)

    def schedule_pulse(self, pulse: Pulse, q: deque): # Should only recieve false pulse
        # c[pulse.t] += 1
        p = self.P[pulse.t]
        #printp(pulse, self)
        q.extend(map(lambda x: (p, x), self.observors))

    def add_observor(self, o):
        self.observors.append(o) # o observes us
        o.observe(self)

    def observe(self, o): # we observe o
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {len(self.observors)})"



class FF(Module):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.mem = False

    def schedule_pulse(self, pulse: Pulse, q: deque):
        #printp(pulse, self)
        # c[pulse.t] += 1
        if pulse.t == False:
            self.mem = not self.mem
            p = self.P[self.mem]
            q.extend(map(lambda x: (p, x), self.observors))

class Con(Module):
    mem: dict[str, bool]

    def __init__(self, name) -> None:
        super().__init__(name)
        self.mem = {}

    def observe(self, o):
        self.mem[o.name] = False # register low pulse

    def schedule_pulse(self, pulse: Pulse, q: deque):
        #printp(pulse, self)
        # c[pulse.t] += 1
        self.mem[pulse.i.name] = pulse.t
        p = self.P[not (pulse.t and all(self.mem.values()))]
        q.extend(map(lambda x: (p, x), self.observors))


class Rx(Module):
    def schedule_pulse(self, pulse: Pulse, q: deque):
        if pulse.t == False:
            raise Exception(i)
        return super().schedule_pulse(pulse, q)

def parse_line(l: str):
    lhs, rhs = l.split("->", 1)
    name = lhs.strip()
    if name == "broadcaster":
        typ = Module
    else:
        typ, name = {"%": FF, "&": Con}[name[0]], name[1:]

    return (typ(name), rhs.strip().split(", "))

mods = mapper.of(open("day20/input.txt", "r").readlines()) | str.strip | parse_line >= list

nmods = mapper.of(mods) | (lambda x: (x[0].name, x[0])) >= dict
nmods["output"] = Module("output")

@star
def build_module(mod, ch):
    consume(map(mod.add_observor, map(lambda n: nmods.get(n) or Module(n), ch)))

mapper.of(mods) | build_module >= consume

b = nmods["broadcaster"]
F = Pulse(False, Module("button"))

def one_cycle(q):
    q.append((F, b))
    while q:
        p, curr = q.popleft()
        curr.schedule_pulse(p, q)

q = deque()

i = 1
while True:
    one_cycle(q)
    i += 1

# 5 minutes not terminating

# one_cycle(q)
# print("===")
# one_cycle(q)
# print("===")
# one_cycle(q)
# print("===")
# one_cycle(q)
# print(c[0] * c[1])

# The solution is in viz.py!!!
