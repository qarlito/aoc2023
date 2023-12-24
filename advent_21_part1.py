

s = '''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''


from advent_input_21 import s

d = list()
STARTPOS = None
for rownum, line in enumerate(s.strip().splitlines()):
    row = list()
    d.append(row)
    for colnum, c in enumerate(line.strip()):
        if c == 'S':
            assert STARTPOS is None
            STARTPOS = (rownum, colnum)
        row.append(c)

NUM_ROWS = len(d)
NUM_COLS = len(d[0])

def find_nonrock_neighbours(position):
    rownum, colnum = position
    result = set()
    if rownum>0 and d[rownum-1][colnum] != '#':
        result.add((rownum-1, colnum))
    if rownum<NUM_ROWS-1 and d[rownum+1][colnum] != '#':
        result.add((rownum+1, colnum))
    if colnum>0 and d[rownum][colnum-1] != '#':
        result.add((rownum, colnum-1))
    if colnum<NUM_COLS-1 and d[rownum][colnum+1] != '#':
        result.add((rownum, colnum+1))
    return result

def draw_map(positions):
    for rownum in range(NUM_ROWS):
        row = list()
        for colnum in range(NUM_COLS):
            if (rownum, colnum) in positions:
                row.append('O')
            else:
                row.append(d[rownum][colnum])
        print(''.join(row))

positions = {STARTPOS}
for step in range(1,65):
    print(f'\nSTEP {step}')
    new_positions = set()
    for position in positions:
        new_positions.update(find_nonrock_neighbours(position))
    positions = new_positions
    #draw_map(positions)
    print(f'After step {step} I reach {len(positions)} positions.')


