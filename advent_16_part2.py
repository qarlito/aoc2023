
s = r'''
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
'''


from advent_input_16 import s

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

m = s.strip().splitlines()
num_cols = len(m[0])
num_rows = len(m)


def evolve(beams, cache):
    new_beams = set()
    for beam in beams:
        row, col, direction = beam
        if direction == LEFT:
            col -= 1
        elif direction == RIGHT:
            col += 1
        elif direction == UP:
            row -= 1
        elif direction == DOWN:
            row += 1
        else:
            raise Exception(f'Impossible direction {direction}')

        if col<0 or row<0 or col>=num_cols or row>=num_rows:
            # Beam disappears
            continue
        if (row, col, direction) in cache:
            # Beam disappears
            continue

        cache.add((row, col, direction))

        cell = m[row][col]
        if cell == '-':
            if direction in [UP, DOWN]:
                new_directions = [LEFT, RIGHT]
            else:
                new_directions = [direction]
        elif cell == '|':
            if direction in [LEFT, RIGHT]:
                new_directions = [UP, DOWN]
            else:
                new_directions = [direction]
        elif cell == '/':
            new_directions = [{LEFT:DOWN, UP:RIGHT, RIGHT:UP, DOWN:LEFT}[direction]]
        elif cell == '\\':
            new_directions = [{LEFT:UP, DOWN:RIGHT, RIGHT:DOWN, UP:LEFT}[direction]]
        else:
            assert cell == '.'
            new_directions = [direction]

        for new_direction in new_directions:
            new_beams.add((row, col, new_direction))

    return new_beams


def get_num_energized(start):
    beams = [start]
    cache = set()

    while len(beams)>0:
        beams = evolve(beams, cache)

    energized = set()
    for (row, col, direction) in cache:
        assert 0 <= row < num_rows
        assert 0 <= col < num_cols
        energized.add((row,col))

    return len(energized)


max_energized = 0

for row in range(num_rows):
    max_energized = max(max_energized, get_num_energized((row, -1, RIGHT)))
    max_energized = max(max_energized, get_num_energized((row, num_cols, LEFT)))

for col in range(num_cols):
    max_energized = max(max_energized, get_num_energized((-1, col, DOWN)))
    max_energized = max(max_energized, get_num_energized((num_rows, col, UP)))

print(f'MAX = {max_energized}')
