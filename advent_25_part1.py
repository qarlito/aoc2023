s = '''jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr'''


from advent_input_25 import s

import networkx as nx
G = nx.Graph()

for line in s.strip().splitlines():
    source, targets = line.split(':')
    for target in targets.strip().split(' '):
        G.add_edge(source, target)


print('G is connected: ', nx.is_connected(G))

cut = nx.minimum_edge_cut(G)
assert len(cut) == 3
print('Found cut of len 3')

print(f'Removing edges {cut}')
G.remove_edges_from(cut)

assert nx.is_connected(G) is False
assert nx.number_connected_components(G) == 2
c1, c2 = nx.connected_components(G)
print(f'Two remaining parts of size {len(c1)} and {len(c2)}. Product is {len(c1)*len(c2)}')

