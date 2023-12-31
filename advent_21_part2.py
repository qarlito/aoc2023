
from advent_input_21 import s

# Read the template for a single cell
d = s.strip().splitlines()
NUM_ROWS = len(d)
NUM_COLS = len(d[0])
assert NUM_ROWS == NUM_COLS
assert NUM_ROWS % 2 == 1
STARTPOS_IN_CELL = ((NUM_ROWS - 1)//2, (NUM_COLS - 1)//2)
assert d[STARTPOS_IN_CELL[0]][STARTPOS_IN_CELL[1]] == 'S'
d = s.strip().replace('S','.').splitlines()


# Find non-rock neighbours in a single cell
def find_nonrock_neighbours(position):
    rownum, colnum = position
    result = set()
    if rownum>0 and 0<=colnum<=NUM_COLS-1 and d[rownum-1][colnum] != '#':
        result.add((rownum-1, colnum))
    if rownum<NUM_ROWS-1 and 0<=colnum<=NUM_COLS-1 and d[rownum+1][colnum] != '#':
        result.add((rownum+1, colnum))
    if colnum>0 and 0<=rownum<=NUM_ROWS-1 and d[rownum][colnum-1] != '#':
        result.add((rownum, colnum-1))
    if colnum<NUM_COLS-1 and 0<=rownum<=NUM_ROWS-1 and d[rownum][colnum+1] != '#':
        result.add((rownum, colnum+1))
    return result


def calculate_steady_state(startposition):
    steps = 0
    positions = {startposition}
    count_two_ago = count_one_ago = -1
    special_counts = {65: None, 131:None, 196:None}
    while len(positions) > count_two_ago:
        count_two_ago = count_one_ago
        count_one_ago = len(positions)
        new_positions = set()
        for position in positions:
            new_positions.update(find_nonrock_neighbours(position))
        positions = new_positions
        steps += 1
        if steps in [65, 131, 196]:
            special_counts[steps] = len(positions)
            print(f'  Finished step {steps} - counter = {len(positions)}')
    return steps-2, count_two_ago, count_one_ago, special_counts


def print_steady_state(description, startposition):
    print(f'\nStarting {description} at position {startposition[0]}, {startposition[1]}')
    steps, total, next_total, special_counts = calculate_steady_state(startposition)
    print(f'Finish   {description}: Needed {steps} steps to reach steady state {total}/{next_total} cells')
    return steps, total, next_total, special_counts


def print_info():
    print(f'WORKING WITH SIZE {NUM_ROWS}')

    print_steady_state('S ', (-1,           NUM_COLS//2))
    print_steady_state('E ', (NUM_ROWS//2, -1))
    print_steady_state('N ', (NUM_ROWS,  NUM_COLS//2))
    print_steady_state('W ', (NUM_ROWS//2, NUM_COLS))

    print_steady_state('SE', (-1,           0))
    print_steady_state('SW', (-1,           NUM_COLS-1))
    print_steady_state('NE', (NUM_ROWS,  0))
    print_steady_state('NW', (NUM_ROWS,  NUM_COLS-1))


def calculate(size, numsteps):

    print(f'Size={size} - Numsteps={numsteps}')

    assert size % 2 == 1
    if numsteps % 2 != 1:
        print('ERROR - numsteps should be odd')

    # Central cell
    # Consider it completed assuming is large

    # Horizontal + vertical
    # Start at      (size+1)/2 + (cells-1).size
    # Complete at   2.size - 2 + (cells-1).size
    num_E_cells_completed = (numsteps - 2*size + 2)//size + 1
    num_E_cells_started = (numsteps-(size+1)//2)//size + 1
    num_E_cells_in_progress = num_E_cells_started - num_E_cells_completed
    if num_E_cells_in_progress != 1:
        print('ERROR - more than 1 HV cell in progress')
    E_cell_in_progress_steps = numsteps - ((size+1)//2 + (num_E_cells_started - 1) * size) + 1
    num_E_cells_no_corners_completed = num_E_cells_completed//2
    num_E_cells_with_corners_completed = num_E_cells_completed - num_E_cells_no_corners_completed
    print(f'\nHor + Vert')
    print(f'  {num_E_cells_started} cells started')
    print(f'  {num_E_cells_with_corners_completed} cells completed (HV with corners) in directions E,W,N,S')
    print(f'  {num_E_cells_no_corners_completed} cells completed (HV no corners) in directions E,W,N,S')
    print(f'  1 cell in progress in each of the 4 quadrants')
    print(f'      -> This cell has finished {E_cell_in_progress_steps} steps')

    # X nocorners
    # Start at    size + 1 + 2.(cells-1).size
    # Complete at 3.size - 2 + 2.(cells-1).size]
    num_X_rays_no_corners_started = (numsteps - size - 1) // (2*size) + 1
    num_X_rays_no_corners_completed = (numsteps - 3*size + 2) // (2*size) + 1
    num_X_cells_no_corners_started = num_X_rays_no_corners_started * num_X_rays_no_corners_started
    num_X_cells_no_corners_completed = num_X_rays_no_corners_completed * num_X_rays_no_corners_completed
    num_X_cells_no_corners_busy = num_X_cells_no_corners_started - num_X_cells_no_corners_completed

    if num_X_rays_no_corners_started - num_X_rays_no_corners_completed != 1:
        print('ERROR - more than 1 X nocorner cell in progress')
    X_cell_no_corners_in_progress_steps = numsteps - (size + 1 + 2*(num_X_rays_no_corners_started-1)*size) + 1

    print(f'\nX nocorners')
    print(f'  {num_X_rays_no_corners_started} rays started')
    print(f'  {num_X_rays_no_corners_completed} rays completed')
    print(f'  {num_X_cells_no_corners_completed} cells completed in each of the 4 quadrants')
    print(f'  {num_X_cells_no_corners_busy} cells in progress in each of the 4 quadrants')
    print(f'    -> Each such cell has finished {X_cell_no_corners_in_progress_steps} steps')

    # X corners
    # Start at      2.size + 1 + 2.(cells-1).size
    # Complete at   4.size - 2 + 2.(cells-1).size
    num_X_rays_corners_started = (numsteps - 2*size - 1) // (2*size) + 1
    num_X_rays_corners_completed = (numsteps - 4*size + 2) // (2*size) + 1
    num_X_cells_corners_started = num_X_rays_corners_started * (num_X_rays_corners_started + 1)
    num_X_cells_corners_completed = num_X_rays_corners_completed * (num_X_rays_corners_completed + 1)
    num_X_cells_corners_busy = num_X_cells_corners_started - num_X_cells_corners_completed

    if num_X_rays_corners_started - num_X_rays_corners_completed != 1:
        print('ERROR - more than 1 X corner cell in progress')
    X_cell_corners_in_progress_steps = numsteps - (2*size + 1 + 2*(num_X_rays_corners_started-1)*size) + 1

    print(f'\nX corners')
    print(f'  {num_X_rays_corners_started} rays started')
    print(f'  {num_X_rays_corners_completed} rays completed')
    print(f'  {num_X_cells_corners_completed} cells completed in each of the 4 quadrants')
    print(f'  {num_X_cells_corners_busy} cells in progress in each of the 4 quadrants')
    print(f'    -> Each such cell has finished {X_cell_corners_in_progress_steps} steps')

SIZE = 131
NUMSTEPS = 26501365

if __name__ == '__main__':
    print_info()
    print()
    print('=' * 40)
    print()
    calculate(SIZE, NUMSTEPS)


output = '''
TYPE,CELLS,POS PER CELL,QUADRANTS,,,
,,,,,
central nocorner,1,7255,1,,7255
,,,,,
HV nocorner,101149,7255,4,,2935343980
HV corner,101150,7262,4,,2938205200
HV incomplete S,1,5474,1,,5474
HV incomplete E,1,5467,1,,5467
HV incomplete N,1,5457,1,,5457
HV incomplete W,1,5464,1,,5464
,,,,,,
X nocorner,10231120201,7255,4,,296907108233020
X nocorner SE,202299,6371,1,,1288846929
X nocorner SW,202299,6358,1,,1286217042
X nocorner NE,202299,6351,1,,1284800949
X nocorner NW,202299,6361,1,,1286823939
,,,,,,
X corner,10231221350,7262,4,,297196517774800
X corner SE,202300,917,1,,185509100
X corner SW,202300,935,1,,189150500
X corner NE,202300,919,1,,185913700
X corner NW,202300,913,1,,184699900
'''

print()
print('=' * 40)
for row in output.splitlines():
    for item in row.split(','):
        if item!='':
            print(f'{item:>16} ', end='')
    print()

total = 0
for row in output.splitlines():
    countstr = row.strip().split(',')[-1]
    if countstr != '':
        total += int(countstr)

print()
print(f'Total: {total}')
