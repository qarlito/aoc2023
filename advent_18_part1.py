s = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''

from advent_input_18 import s

instructions = list()

for line in s.strip().splitlines():
    direction, countstr, _ = line.split(' ')
    instructions.append((direction, int(countstr)))

assert instructions[0][0] == 'R' and instructions[-1][0] == 'U'

min_row = max_row = min_col = max_col = 0
row = col = 0
for direction, count in instructions:
    if direction=='U':
        row -= count
    elif direction=='D':
        row += count
    elif direction=='R':
        col += count
    elif direction=='L':
        col -= count
    else:
        raise Exception('Illegal input')
    min_row = min(min_row, row)
    min_col = min(min_col, col)
    max_row = max(max_row, row)
    max_col = max(max_col, col)

num_rows = (max_row-min_row+1)
num_cols = (max_col-min_col+1)

m = list()
for row in range(num_rows):
    m.append(['.'] * num_cols)

row = -min_row
col = -min_col
prev_direction = instructions[-1][0]
for direction, count in instructions:
    assert direction != prev_direction
    assert {'U':'D', 'D':'U', 'L':'R', 'R':'L'}[prev_direction] != direction
    if direction=='U':
        for r in range(row-count+1, row):
            m[r][col] = '|'
        m[row][col] = {'L':'L', 'R':'J'}[prev_direction]
        row -= count
    elif direction=='D':
        for r in range(row+1, row+count):
            m[r][col] = '|'
        m[row][col] = {'L':'F', 'R':'7'}[prev_direction]
        row += count
    elif direction=='R':
        for c in range(col+1, col+count):
            m[row][c] = '-'
        m[row][col] = {'U':'F', 'D':'L'}[prev_direction]
        col += count
    elif direction=='L':
        for c in range(col-count+1, col):
            m[row][c] = '-'
        m[row][col] = {'U':'7', 'D':'J'}[prev_direction]
        col -= count
    else:
        raise Exception('Illegal input')
    prev_direction = direction

for row in m:
    print(''.join(row))
