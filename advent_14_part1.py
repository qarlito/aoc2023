s = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''

from advent_input_14 import s


def flip(m):
    result = list()
    for col in range(len(m[0])):
        col_content = ''.join([m[row][col] for row in range(len(m))])
        result.append(col_content)
    return result

def print_m(m):
    print('\n'.join(m))

m_input = s.splitlines()

def tilt_to_left(m):
    m_tilted_to_left = list()
    for row in m:
        result = list()
        last_stable_pos = -1
        for i, c in enumerate(row):
            if c=='O':
                result.append('.')
                last_stable_pos += 1
                result[last_stable_pos] = 'O'
            elif c=='#':
                last_stable_pos = i
                result.append(c)
            elif c=='.':
                result.append(c)
            else:
                raise Exception('Error')
        m_tilted_to_left.append(''.join(result))
    return m_tilted_to_left

def score(m):
    result = 0
    for n, row in enumerate(m):
        result += row.count('O') * (len(m)-n)
    return result

m_from_top = flip(m_input)
m_from_top_tilted = tilt_to_left(m_from_top)
m2 = flip(m_from_top_tilted)
sc = score(m2)

DEBUG = False
if DEBUG:
    print_m(m_input)
    print()
    print_m(m_from_top)
    print()
    print_m(m_from_top_tilted)
    print()
    print_m(m2)
    print()

print(f'Score: {sc}')
