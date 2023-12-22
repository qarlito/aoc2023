import re
from pprint import pprint

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

UP = (-1,0,'U')
DOWN = (1,0,'D')
LEFT = (0,-1,'L')
RIGHT = (0,1,'R')

oldpos = (0,0)
path = list()
for line in s.strip().splitlines():
    _, r = line.split('#')
    assert len(r) == 7
    assert r[-1] == ')'
    dist = int(r[:5], 16)
    direction = {'0':RIGHT, '1':DOWN, '2':LEFT, '3':UP}[r[5]]

    delta = (direction[0]*dist, direction[1]*dist)
    newpos = (oldpos[0]+delta[0], oldpos[1]+delta[1])
    path.append((oldpos, newpos, delta, dist, direction))
    oldpos = newpos

assert path[-1][1][0] == 0
assert path[-1][1][1] == 0

row_positions = sorted(set(map(lambda entry: entry[0][0], path)))
col_positions = sorted(set(map(lambda entry: entry[0][1], path)))

smallpath = list()
for (oldpos, newpos, delta, dist, direction) in path:
    small_oldrow = row_positions.index(oldpos[0])
    small_oldcol = col_positions.index(oldpos[1])
    small_newrow = row_positions.index(newpos[0])
    small_newcol = col_positions.index(newpos[1])
    small_dist = (small_newrow-small_oldrow)*direction[0] + (small_newcol-small_oldcol)*direction[1]
    assert small_dist>0
    smallpath.append((small_dist, direction))

small_s =''
for small_dist, direction in smallpath:
    small_s += f'{direction[2]} {small_dist}\n'

instructions = list()

for line in small_s.strip().splitlines():
    direction, countstr = line.split(' ')
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


# Looking at the horizontally expanded row itself, not the area below it
def score(left, right):
    return col_positions[right] - col_positions[left] + 1

INSIDE = object()
OUTSIDE = object()
print()
total = 0
prevbodyrow = '.' * len(m[0])
for rownum in range(len(m)):

    # Determine current row score of horizontally expanded row itself, not the area below it

    currrow = ''.join(m[rownum])
    currrowscore = 0
    offset = 0
    startpos = -1
    status = OUTSIDE
    #print(f'starting row analysis for {currrow}')
    while offset < len(currrow):
        mm = re.search('[^.]', currrow[offset:])
        if mm is None:
            assert status == OUTSIDE
            break
        offset += mm.start()
        if status == OUTSIDE:
            startpos = offset
            if currrow[offset] == 'F':
                mm = re.match('F-*J', currrow[offset:])
                if mm:
                    offset += mm.end()
                    status = INSIDE
                else:
                    mm = re.match('F-*7', currrow[offset:])
                    assert mm is not None
                    offset += mm.end()
                    currrowscore += score(startpos, offset-1)
            elif currrow[offset] == 'L':
                mm = re.match('L-*7', currrow[offset:])
                if mm:
                    offset += mm.end()
                    status = INSIDE
                else:
                    mm = re.match('L-*J', currrow[offset:])
                    assert mm is not None
                    offset += mm.end()
                    currrowscore += score(startpos, offset-1)
            elif currrow[offset] == '|':
                status = INSIDE
                offset += 1
            else:
                raise Exception('Impossible')
        else:
            if currrow[offset] == 'F':
                mm = re.match('F-*7', currrow[offset:])
                if mm:
                    offset += mm.end()
                else:
                    mm = re.match('F-*J', currrow[offset:])
                    assert mm is not None
                    offset += mm.end()
                    currrowscore += score(startpos, offset-1)
                    status = OUTSIDE
                    startpos = -1
            elif currrow[offset] == 'L':
                mm = re.match('L-*J', currrow[offset:])
                if mm:
                    offset += mm.end()
                else:
                    mm = re.match('L-*7', currrow[offset:])
                    assert mm is not None
                    offset += mm.end()
                    currrowscore += score(startpos, offset-1)
                    status = OUTSIDE
                    startpos = -1
            elif currrow[offset] == '|':
                status = OUTSIDE
                offset += 1
                currrowscore += score(startpos, offset-1)
                startpos = -1
            else:
                raise Exception('Impossible')

    total += currrowscore    


    # Now looking at space between this row and the next row when vertically expanding
    bodyrow = ''.join(m[rownum])
    bodyrow = re.sub('F-*7', lambda match: '|' + '.'*(len(match.group())-2) + '|', bodyrow)
    bodyrow = re.sub('F-*J', lambda match: '|' + '.'*(len(match.group())-1), bodyrow)
    bodyrow = re.sub('L-*7', lambda match: '.'*(len(match.group())-1) + '|', bodyrow)
    bodyrow = re.sub('L-*J', lambda match: '.'*(len(match.group())), bodyrow)

    if rownum == len(m)-1:
        bodyheight = 0
    else:
        bodyheight = row_positions[rownum+1] - row_positions[rownum] - 1
    offset = 0
    while bodyrow.find('|', offset) != -1:
        left = bodyrow.index('|', offset)
        right = bodyrow.index('|', left+1)
        total += (col_positions[right] - col_positions[left] + 1) * bodyheight
        offset = right + 1

print(f'TOTAL = {total}')
