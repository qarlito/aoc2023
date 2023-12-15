
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


FLIP = {'#':'.', '.':'#'}

def get_pimped_row(structure, rownum, pimprow, pimpcol):
    row = structure[rownum]
    if rownum == pimprow:
        row = row[:pimpcol] + FLIP[row[pimpcol]] + row[pimpcol+1:]
    return row


def find_mirror_line(structure, pimprow=None, pimpcol=None, forbidden_result=-1):
    # Attempt to mirror before row
    for rownum in range(1, len(structure)):
        is_mirror = True
        for delta in range(min(rownum, len(structure)-rownum)):
            if get_pimped_row(structure, rownum-1 - delta, pimprow, pimpcol) != get_pimped_row(structure, rownum + delta, pimprow, pimpcol):
                is_mirror = False
        if is_mirror and rownum!=forbidden_result:
            return rownum
    return -1


def find_pimped_mirror(n):
    nonpimped_hmirror = find_mirror_line(hstructures[n])
    nonpimped_vmirror = find_mirror_line(vstructures[n])
    for pimprow in range(len(hstructures[n])):
        for pimpcol in range(len(vstructures[n])):
            mirror = find_mirror_line(vstructures[n], pimpcol, pimprow, nonpimped_vmirror)
            if mirror == -1:
                mirror = 100 * find_mirror_line(hstructures[n], pimprow, pimpcol, nonpimped_hmirror)
            if mirror > 0:
                return mirror
    raise Exception(f'No mirror found {n}')

total = 0
for n in range(len(hstructures)):
    mirror = find_pimped_mirror(n)
    print(f'Puzzle {n} mirror {mirror}')
    total += mirror

print(f'TOTAL = {total}')

