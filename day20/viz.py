from __future__ import annotations

# import networkx as nx
# G = nx.DiGraph()

# False is low
# True is high
from collections import deque, namedtuple
from functools import partial
import operator as op
from itertools import chain
from turtle import color
from more_itertools import consume

from wafle import star, mapper
import graphviz as gv

dot = gv.Digraph()

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

# print(mods)

cmap = {
    Module: "white",
    FF: "green",
    Con: "blue",
    Rx: "red",
}

# G.add_nodes_from(  )



mapper.of(mods) | (lambda x: dot.node(x[0].name, x[0].name, color=cmap[x[0].__class__], shape="square")) >= list

a = mapper.of(mods) | (lambda x: mapper.of(x[1]) | (lambda k: dot.edge(x[0].name, k)) >= list) >= list

print(a)
dot.format = "png"
dot.render(directory="day20")

# Visualise
# Notice that the node connected to broadcaster is LSB T flip flop
# then notice that the central node simply sends high pulse when reset
# flip flops work on low pulses!
# hence all edges outgoing from central nodes are useless
# but the state of the "bits" which have edges towards the central node
# mean that the central node will send a low pulse only when all of those flip flops
# are in the on state (having sent a high pulse earlier)
# Notice that the edges from central node are set up in such a way
# that when it sends a low pulse all the "bits" go to zero by sort of "overflowing"
# Hence the period of the graph is carefully engineered
#
# We can see convert the subgraph into 4 11 bit numbers
# These are obtained by looking at which "bits" point towards the central conjunction node
# start from lowest node and go up to topmost (MSB to LSB)
# Here are my conversions
# >>> 0b111010111001
# 3769
# >>> a = _
# >>> b = 0b111101011011
# >>> b
# 3931
# >>> c = 0b111100010111
# >>> c
# 3863
# >>> d = 0b111011010101
# >>> d
# 3797
# take the lcm of a,b,c,d