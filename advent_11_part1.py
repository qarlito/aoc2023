from pprint import pprint

s = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''

from advent_input_11 import s

m = list()
for line in s.strip().splitlines():
    m.append([c for c in line.strip()])

num_rows = len(m)
num_cols = len(m[0])

empty_cols = list()
for col in range(num_cols):
    if all([m[row][col]=='.' for row in range(num_rows)]):
        empty_cols.append(col)

empty_rows = list()
for row in range(num_rows):
    if all([c=='.' for c in m[row]]):
        empty_rows.append(row)

#pprint(m)
#pprint(empty_rows)
#pprint(empty_cols)


# Expand the universe

expanded_num_rows = num_rows + len(empty_rows)
expanded_num_cols = num_cols + len(empty_cols)
expanded_m = list()
col_offsets = [-1] + empty_cols + [expanded_num_cols]

for row in range(num_rows):
    if row in empty_rows:
        expanded_m.append(['.'] * expanded_num_cols)
        expanded_m.append(['.'] * expanded_num_cols)
    else:
        parts = [''.join(m[row][start+1:end]) for (start,end) in zip(col_offsets[:-1], col_offsets[1:])]
        expanded_m.append([c for c in '..'.join(parts)])

for row in expanded_m:
    print(''.join(row))

galaxies = list()
for row_num, row in enumerate(expanded_m):
    for col_num, value in enumerate(row):
        if value == '#':
            galaxies.append((row_num, col_num))

print(galaxies)

total = 0
count = 0
for n1 in range(len(galaxies)-1):
    for n2 in range(n1+1, len(galaxies)):
        row1, col1 = galaxies[n1]
        row2, col2 = galaxies[n2]
        distance = (abs(row2-row1) + abs(col2-col1))
        print(f'{count}.  {galaxies[n1]} -> {galaxies[n2]} = {distance}')
        total += distance
        count += 1

print(f'total = {total}')

