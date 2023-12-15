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


# A B C   ==>   C F
# D E F         B E
#               A D


def rot90_counter_clock(m):
    result = list()
    for col in range(len(m[0])-1, -1, -1):
        col_content = ''.join([m[row][col] for row in range(len(m))])
        result.append(col_content)
    return result

def rot90_clock(m):
    result = list()
    for col in range(len(m[0])):
        col_content = ''.join([m[len(m)-1-row][col] for row in range(len(m))])
        result.append(col_content)
    return result


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

def get_score(m):
    result = 0
    for n, row in enumerate(m):
        result += row.count('O') * (len(m)-n)
    return result

def do_cycle(m):
    m = rot90_counter_clock(m)
    m = tilt_to_left(m)
    m = rot90_clock(m)
    m = tilt_to_left(m)
    m = rot90_clock(m)
    m = tilt_to_left(m)
    m = rot90_clock(m)
    m = tilt_to_left(m)
    m = rot90_clock(rot90_clock(m))
    return m

m = m_input
m_to_step_cache = dict()
step_to_score_cache = dict()

BIG_NUMBER = 1000000000
#BIG_NUMBER = 20
n = 0
while n<1000:
    n += 1
    m = do_cycle(m)
    mtup = tuple(m)
    if mtup in m_to_step_cache:
        cycle_start = m_to_step_cache[mtup]
        print(f'Found cycle! value({n}) == value ({cycle_start})')
        equivalent_step = cycle_start + ((BIG_NUMBER - cycle_start) % (n - cycle_start))
        score = step_to_score_cache[equivalent_step]
        print(f'Remapping {BIG_NUMBER} to {equivalent_step} having score {score}')
        break
    else:
        m_to_step_cache[mtup] = n
        step_to_score_cache[n] = get_score(m)

