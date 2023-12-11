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

galaxies = list()
for row_num, row in enumerate(m):
    for col_num, value in enumerate(row):
        if value == '#':
            galaxies.append((row_num, col_num))

def num_items_between(items, start, end):
    return [start<item<end for item in items].count(True)


EXPANSION_FACTOR = 1_000_000

total = 0
count = 0
for n1 in range(len(galaxies)-1):
    for n2 in range(n1+1, len(galaxies)):
        row1, col1 = galaxies[n1]
        row2, col2 = galaxies[n2]
        distance = abs(row2-row1) + abs(col2-col1) + (EXPANSION_FACTOR-1) * num_items_between(empty_rows, min(row1,row2), max(row1,row2)) + (EXPANSION_FACTOR-1) * num_items_between(empty_cols, min(col1,col2), max(col1,col2))
        total += distance
        count += 1

print(f'total = {total}')

