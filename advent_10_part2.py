s = '''7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ'''


s = '''...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........'''

s = '''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''

s = '''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L'''

from advent_input_10 import s

from pprint import pprint

CHARS = '|-LJ7F.S'

CONNECTS_DOWN='|7FS'
CONNECTS_UP='|LJS'
CONNECTS_LEFT='-J7S'
CONNECTS_RIGHT='-LFS'

REAL_SCAN_BOUNDARIES = [set('FJ'), set('L7')]

def read_input(input_str):
    m = list()
    start = None
    for row, row_str in enumerate(input_str.strip().splitlines()):
        row_list = list()
        m.append(row_list)
        for col, char in enumerate(row_str.strip()):
            assert char in CHARS
            if char == 'S':
                assert start is None
                start_location = (row, col)
            row_list.append(char)
    assert all([len(row_list) == len(m[0]) for row_list in m])
    return m, start_location


def connects(m, row1, col1, row2, col2):
    if min(row1, col1, row2, col2) < 0:
        return False
    if max(row1, row2) >= len(m):
        return False
    if max(col1, col2) >= len(m[0]):
        return False
    if row1 == row2:
        left_col = min(col1, col2)
        right_col = max(col1, col2)
        assert right_col - left_col == 1
        return m[row1][left_col] in CONNECTS_RIGHT and m[row1][right_col] in CONNECTS_LEFT
    if col1 == col2:
        upper_row = min(row1, row2)
        lower_row = max(row1, row2)
        assert lower_row - upper_row == 1
        return m[upper_row][col1] in CONNECTS_DOWN and m[lower_row][col1] in CONNECTS_UP
    return False


def find_connected_neighbours(m, location):
    row, col = location
    result = list()
    up = down = left = right = False
    if connects(m, row, col, row+1, col):
        result.append((row+1, col))
        down = True
    if connects(m, row, col, row-1, col):
        result.append((row-1, col))
        up = True
    if connects(m, row, col, row, col+1):
        result.append((row, col+1))
        right = True
    if connects(m, row, col, row, col-1):
        result.append((row, col-1))
        left = True
    assert len(result) == 2
    if up and down:
        replacement_char = '|'
    elif up and right:
        replacement_char = 'L'
    elif up and left:
        replacement_char = 'J'
    elif right and left:
        replacement_char = '-'
    elif right and down:
        replacement_char = 'F'
    elif left and down:
        replacement_char = '7'
    assert m[row][col] in ['S', replacement_char]
    return result, replacement_char


def extend_path(m, path):
    last_location = path[-1]
    candidate_locations, replacement_char = find_connected_neighbours(m, last_location)
    extended_location = candidate_locations[0]
    if len(path) > 1 and extended_location == path[-2]:
       # Make sure we don't go backwards
           extended_location = candidate_locations[1]
    path.append(extended_location)


m, start_location = read_input(s)

print(f'START = {start_location}')


result, replacement_char = find_connected_neighbours(m, start_location)
print(f'  -> replacing with {replacement_char}')
m[start_location[0]][start_location[1]] = replacement_char


path = [start_location]
while len(path)==1 or path[0] != path[-1]:
    extend_path(m, path)

#for coord in path:
#    print(m[coord[0]][coord[1]])

assert (len(path)-1) % 2 == 0
print(f'PATH LEN = {(len(path)-1) // 2}')


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
        if (row, col) in path:
            path_map[row][col] = 'x'
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


#print()
#print('\n'.join([''.join(x) for x in path_map]))
#print()
#pprint(hor_map)


total = 0
for row_list in hor_map:
    total += row_list.count(True)
print(total)
