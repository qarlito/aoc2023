s = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''

s = '''
1191000
1110000
8111100
1111101
0101100
0101100
1111111
'''
from advent_input_17 import s

m = list()
for row in s.strip().splitlines():
    m.append([i for i in map(int, row)])
NUM_ROWS = len(m)
NUM_COLS = len(m[0])
assert NUM_ROWS == NUM_COLS

# Create diagonal path just as a start point
diag_cost = 0
for row in range(1,NUM_ROWS):
    diag_cost += m[row][row-1] + m[row][row]
print(f'Diag cost is {diag_cost}')

NODIRECTION = 'nodirection'
LEFT = (0,-1)
RIGHT = (0,1)
UP = (-1,0)
DOWN = (1,0)

DIRECTIONS = [RIGHT, DOWN, LEFT, UP]
CANDIDATE_DIRECTION_MAP = { NODIRECTION:frozenset({LEFT,RIGHT,UP,DOWN}),
                            RIGHT:frozenset({RIGHT,UP,DOWN}),
                            LEFT:frozenset({LEFT,UP,DOWN}),
                            UP:frozenset({LEFT,RIGHT,UP}),
                            DOWN:frozenset({LEFT,RIGHT,DOWN}) }
CANDIDATE_DIRECTION_MAP_AFTER_3 = { RIGHT:frozenset({UP,DOWN}),
                                    LEFT:frozenset({UP,DOWN}),
                                    UP:frozenset({LEFT,RIGHT}),
                                    DOWN:frozenset({LEFT,RIGHT}) }
def get_valid_directions(direction, direction_count):
    if direction_count == 3:
        return CANDIDATE_DIRECTION_MAP_AFTER_3[direction]
    else:
        return CANDIDATE_DIRECTION_MAP[direction]
    

# Entries are written (row, col, direction_of_last_move_to_this_cell, direction_count_including_last_move_to_this_cell, cost_including_this_cell)
START = (0, 0, NODIRECTION, 0, 0, tuple())
cache = dict()  # (row, col, direction_of_last_move_to_this_cell, direction_count_including_last_move_to_this_cell) -> (cost, path)

winner = {'cost':diag_cost, 'path':None}

def get_new_positions(position):
    row, col, direction, direction_count, cost, path = position
    new_positions = set()
    for new_direction in get_valid_directions(direction, direction_count):
        new_row = row + new_direction[0]
        new_col = col + new_direction[1]
        if new_row<0 or new_col<0 or new_row>=NUM_ROWS or new_col>=NUM_COLS:
            # Illegal position
            continue
        new_cost = cost + m[new_row][new_col]
        if new_cost >= winner['cost']:
            # Not better
            continue
        new_direction_count = direction_count+1 if direction == new_direction else 1
        cache_key = (new_row, new_col, new_direction, new_direction_count)
        cached_cost = cache.get(cache_key, -1)
        if cached_cost != -1 and cached_cost <= new_cost:
            # We have a cheaper path to this position
            continue
        cache[cache_key] = new_cost
        new_path = path+((new_row,new_col),)
        if new_row==NUM_ROWS-1 and new_col==NUM_COLS-1:
            # No need to further grow
            if new_cost < winner['cost']:
                winner['cost'] = new_cost
                winner['path'] = new_path
                print(f'Found path with cost {winner["cost"]}')
            continue
        else:
            new_positions.add((new_row, new_col, new_direction, new_direction_count, new_cost, new_path))
    return new_positions

positions = {START}
while True:
    new_positions = set()
    for position in positions:
        new_positions = new_positions.union(get_new_positions(position))
        #print(f'{new_positions}')
    if len(new_positions) == 0:
        # No more ways to extend
        break
    positions = new_positions

print('\nWINNER\n')
for row in range(NUM_ROWS):
    line = ''
    for col in range(NUM_COLS):
        if (row, col) in winner['path']:
            line += str(m[row][col])
        else:
            line += '.'
    print(line)


cache = dict()
