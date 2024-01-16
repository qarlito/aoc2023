import pprint
import itertools

s = '''
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#'''



from advent_input_23 import s

# Strategy

# Find the points where you can choose.
# Assert that choice points are one-way (i.e. 1 or 2 come in; 2 or 3 go out)

# Construct a directed graph. Start and end are 2 named nodes.
# Every choice point is a node, connected to 1 or 2 incoming nodes, and 2 or 3 outgoing nodes
# Check if it is a directed acyclic graph (probably it is).
# Every edge of the graph has a weight corresponding with the distance between its nodes

# Find longest path in this graph.

d = s.strip().splitlines()
NUM_ROWS = len(d)
NUM_COLS = len(d[0])
assert len(set([len(row) for row in d])) == 1
assert d[0].count('.') == 1
assert d[-1].count('.') == 1

IN = 'i'
OUT = 'o'
UP = (-1,0)
DOWN = (1,0)
LEFT = (0,-1)
RIGHT = (0,1)
DIRECTIONS = [DOWN, RIGHT, LEFT, UP]
NUM_DIRECTIONS = len(DIRECTIONS)

nodes = dict()   # Coord -> { IN:  {DIR->((node_row,node_col),dist),...},
                 #            OUT: {DIR->(node,dist),...} }
                 # node is None if it is not yet known

START_NODE = (0, d[0].index('.'))
nodes[START_NODE] = {OUT:{DOWN:None}, IN:dict()}
END_NODE   = (NUM_ROWS-1, d[-1].index('.'))
nodes[END_NODE] = {OUT:dict(), IN:{UP:None}}


for row_num in range(1, NUM_ROWS-1):
    for col_num in range(1, NUM_COLS-1):
        assert d[row_num][col_num] in '#.v^<>'
        if d[row_num][col_num] == '#':
            continue
        neighbours = [d[row_num-1][col_num], d[row_num+1][col_num], d[row_num][col_num-1], d[row_num][col_num+1]]
        num_dots = neighbours.count('.')
        assert num_dots <= 2
        num_borders = neighbours.count('#')
        assert num_borders <= 2
        incoming_dirs = list()
        outgoing_dirs = list()
        if neighbours[0] == 'v':
            incoming_dirs.append(UP)
        if neighbours[0] == '^':
            outgoing_dirs.append(UP)
        if neighbours[1] == '^':
            incoming_dirs.append(DOWN)
        if neighbours[1] == 'v':
            outgoing_dirs.append(DOWN)
        if neighbours[2] == '>':
            incoming_dirs.append(LEFT)
        if neighbours[2] == '<':
            outgoing_dirs.append(LEFT)
        if neighbours[3] == '<':
            incoming_dirs.append(RIGHT)
        if neighbours[3] == '>':
            outgoing_dirs.append(RIGHT)
        assert len(incoming_dirs) + num_dots <= 2
        assert len(outgoing_dirs) + num_dots <= 2
        if num_borders < 2:
            assert num_dots == 0
            assert len(incoming_dirs) >= 1
            assert len(outgoing_dirs) >= 1
            incoming_info = dict(zip(incoming_dirs, itertools.repeat(None)))
            outgoing_info = dict(zip(outgoing_dirs, itertools.repeat(None)))
            nodes[(row_num, col_num)] = {IN: incoming_info, OUT: outgoing_info}

''' return ((row, col), distance, direction of entry to target) '''
def find_next_node(from_node, out_dir):
    pos = (from_node[0] + out_dir[0], from_node[1] + out_dir[1])
    direction = out_dir
    distance = 1
    while True:
        # Calculate next position
        if direction in (UP, DOWN):
            try_directions = (direction, LEFT, RIGHT)
        else:
            try_directions = (direction, UP, DOWN)

        found_next = False
        for try_direction in try_directions:
            try_pos = (pos[0] + try_direction[0], pos[1] + try_direction[1])
            if d[try_pos[0]][try_pos[1]] != '#':
                distance += 1
                found_next = True
                pos = try_pos
                direction = try_direction
                if pos in nodes:
                    return (pos, distance, (-direction[0], -direction[1]))
                break
        assert found_next


for node, node_info in nodes.items():
    for direction, direction_info in sorted(node_info[OUT].items()):
        if not direction_info:
            new_node, distance, in_direction = find_next_node(node, direction)
            node_info[OUT][direction] = (new_node, distance)
            nodes[new_node][IN][in_direction] = (node, distance)

num_nodes_with_2_targets = 0
for node, node_info in nodes.items():
    num_targets = len(node_info[OUT])
    if num_targets == 2:
        num_nodes_with_2_targets += 1
    if node == START_NODE:
        special = ' [START_NODE]'
    elif node == END_NODE:
        special = ' [END_NODE]'
    else:
        special = ''
    print(f'\n({node[0]},{node[1]}){special} has {num_targets} outbound target(s)')
    for direction, direction_info in sorted(node_info[OUT].items()):
        print(f'      ({node[0]},{node[1]})  ->  ({direction_info[0][0]},{direction_info[0][1]})    COST {direction_info[1]}')

print()
pprint.pprint(nodes)

# Exhaustively try all paths by just trying all directions, and asserting we are not making circles
# path = [ (node, cost, last_chosen_direction), (node, cost, last_chosen_direction), ... ]

path = [ (START_NODE, 0, -1) ]
highest_cost = -1

# Backtracking algorithm
while True:

    if len(path) == 0:
        print(f'\nfinished searching. Hi score is {highest_cost}')
        break

    node, cost, direction_num = path.pop()

    if node == END_NODE:
        #if cost > highest_cost:
        #    print()
        #    pprint.pprint([(a,b,DIRECTIONS[c]) for a,b,c in path])
        #    print(f'Reaching {node} with cost {cost}')
        highest_cost = max(cost, highest_cost)
        continue

    new_direction = direction_num + 1
    if new_direction == NUM_DIRECTIONS-1:
        continue
    path.append((node, cost, new_direction))

    new_node, extra_cost = nodes[node][OUT].get(DIRECTIONS[new_direction], (None,None))
    if new_node is not None and new_node not in [n for n,_,_ in path]:
        # We did not visit this node before; let's extend our path
        path.append((new_node, cost+extra_cost, -1))
