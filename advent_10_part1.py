s = '''7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ'''


from advent_input_10 import s

from pprint import pprint

CHARS = '|-LJ7F.S'

CONNECTS_DOWN='|7FS'
CONNECTS_UP='|LJS'
CONNECTS_LEFT='-J7S'
CONNECTS_RIGHT='-LFS'

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
    if connects(m, row, col, row+1, col):
        result.append((row+1, col))
    if connects(m, row, col, row-1, col):
        result.append((row-1, col))
    if connects(m, row, col, row, col+1):
        result.append((row, col+1))
    if connects(m, row, col, row, col-1):
        result.append((row, col-1))
    return result


def extend_path(m, path):
    last_location = path[-1]
    candidate_locations = find_connected_neighbours(m, last_location)
    assert len(candidate_locations) == 2
    extended_location = candidate_locations[0]
    if len(path) > 1 and extended_location == path[-2]:
       # Make sure we don't go backwards
           extended_location = candidate_locations[1]
    path.append(extended_location)


m, start_location = read_input(s)

pprint(m)
print(start_location)

path = [start_location]
while len(path)==1 or path[0] != path[-1]:
    extend_path(m, path)

for coord in path:
    print(m[coord[0]][coord[1]])

assert (len(path)-1) % 2 == 0
print( (len(path)-1) // 2 )
