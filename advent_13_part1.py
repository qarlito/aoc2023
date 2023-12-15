
s = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''

from advent_input_13 import s

hstructures = list()
for line in ('\n'+s).splitlines():
    if line == '':
        hstructure = list()
        hstructures.append(hstructure)
    else:
        hstructure.append(line)

vstructures = list()
for hstructure in hstructures:
    vstructure = [''] * len(hstructure[0])
    vstructures.append(vstructure)
    for hline in hstructure:
        for col, c in enumerate(hline):
            vstructure[col] += c


def find_mirror_line(structure):
    # Attempt to mirror before row
    for rownum in range(1, len(structure)):
        is_mirror = True
        for delta in range(min(rownum, len(structure)-rownum)):
            if structure[rownum-1 - delta] != structure[rownum + delta]:
                is_mirror = False
        if is_mirror:
            return rownum
    return -1

total = 0
for n in range(len(hstructures)):
    mirror = find_mirror_line(vstructures[n])
    if mirror == -1:
        mirror = 100 * find_mirror_line(hstructures[n])
    assert mirror > 0
    print(f'{n} -> {mirror}')
    total += mirror

print(f'MIRROR = {total}')

