s = '''F-----7
|.....|
L-7...|
..|...|
..|...|
F-J.F-J
|...|..
L7..L-7
.|....|
.L----J'''

from advent_18_intermediate_output import s

from pprint import pprint

CHARS = '|-LJ7F.S'

REAL_SCAN_BOUNDARIES = [set('FJ'), set('L7')]

def read_input(input_str):
    m = list()
    for row, row_str in enumerate(input_str.strip().splitlines()):
        row_list = list()
        m.append(row_list)
        for col, char in enumerate(row_str.strip()):
            assert char in CHARS
            row_list.append(char)
    assert all([len(row_list) == len(m[0]) for row_list in m])
    return m

m = read_input(s)


hor_map = list()
path_map = list()
for row in range(len(m)):
    hor_map.append([False] * len(m[0]))
    path_map.append([' '] * len(m[0]))

OUTSIDE = 0
INSIDE = 1
ENTERING_BOUNDARY = 2
LEAVING_BOUNDARY = 3

border_char = None
for row in range(len(m)):
    status = OUTSIDE
    for col in range(len(m[0])):
        if m[row][col] != '.':
            path_map[row][col] = 'x'
            hor_map[row][col] = True
            char = m[row][col]
            if char == '|':
                if status == INSIDE:
                    status = OUTSIDE
                elif status == OUTSIDE:
                    status = INSIDE
                else:
                    raise Exception('Impossible')
            elif char == '-':
                assert status in (ENTERING_BOUNDARY, LEAVING_BOUNDARY)
            else:
                if status == OUTSIDE:
                    status = ENTERING_BOUNDARY
                    border_char = char
                elif status == ENTERING_BOUNDARY:
                    if set([border_char, char]) in REAL_SCAN_BOUNDARIES:
                        status = INSIDE
                    else:
                        status = OUTSIDE
                elif status == INSIDE:
                    status = LEAVING_BOUNDARY
                    border_char = char
                elif status == LEAVING_BOUNDARY:
                    if set([border_char, char]) in REAL_SCAN_BOUNDARIES:
                        status = OUTSIDE
                    else:
                        status = INSIDE
                else:
                    raise Exception('Impossible')
        else:
            assert status in (INSIDE, OUTSIDE)
            hor_map[row][col] = (status == INSIDE)


print()
print('\n'.join([''.join(x) for x in path_map]))
print()
pprint(hor_map)


total = 0
for row_list in hor_map:
    total += row_list.count(True)
print(total)
