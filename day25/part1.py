
from collections import defaultdict, deque
from more_itertools import consume
from networkx import adjacency_matrix

from wafle import mapper, rpartial, star

adj_mat: dict[str, set[str]] = defaultdict(set)

mapper.of(open("day25/input.txt", "r").readlines()) | str.strip | rpartial(str.split, ":") | star(lambda k, v: adj_mat[k].update(v.strip().split())) >= consume

# print(adj_mat)

def connected(a: str, b: str) -> bool:
    return b in adj_mat[a] or a in adj_mat[b]

# import graphviz as gv

# dot = gv.Graph()

# for node, ch in adj_mat.items():
#     dot.node(node, node)
#     for child in ch:
#         dot.node(child, child)
#         dot.edge(node, child)

# dot.format = "svg"
# dot.engine = "neato"
# dot.render(directory="day25")

edges = [("nmv", "thl"), ("vgk", "mbq"), ("fxr", "fzb")] # visually identified


nodes = set()

for node, ch in adj_mat.items():
    nodes.add(node)
    nodes.update(ch)

tot = len(nodes)

for a, b in edges:
    b in adj_mat[a] and adj_mat[a].remove(b)
    a in adj_mat[b] and adj_mat[b].remove(a)

itl = {node: ch.copy() for node, ch in adj_mat.items()}
for node, ch in itl.items():
    for child in ch:
        adj_mat[child].add(node)

# now we posses undirected partitioned graph

q = deque()
vis = set()

def visit(a):
    vis.add(a)
    q.extend(filter(lambda c: c not in vis, adj_mat[a]))

q.append(edges[0][0])

while q:
    curr = q.pop()
    visit(curr)

la = len(vis)
print((tot - la) * la)