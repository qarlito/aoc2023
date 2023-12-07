


def to_coordinates(inputstr):
    result = list()
    for row in inputstr.splitlines():
        rowlist = list()
        result.append(rowlist)
        for symbol in row:
            if symbol.isdigit():
                rowlist.append(int(symbol))
            elif symbol == '.':
                rowlist.append(None)
            else:
                rowlist.append('x')
    return result


def is_symbol(coordinates, row, col):
    print(f'{row}, {col}')
    if row<0 or row>=len(coordinates):
        return False
    if col<0 or col>=len(coordinates[0]):
        return False
    return coordinates[row][col] == 'x'


def touches_symbol(coordinates, row_number, start_pos, end_pos):
    for row in range(row_number-1, row_number+2):
        for col in range(start_pos-1, end_pos+2):
            if is_symbol(coordinates, row, col):
                return True
    return False


def process(coordinates, row_number, start_pos, end_pos):
    if touches_symbol(coordinates, row_number, start_pos, end_pos):
        return int(''.join(map(str, coordinates[row_number][start_pos:end_pos+1])))
    else:
        return 0


s = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''


from advent_input_03 import s

coordinates = to_coordinates(s)

result = 0
for rownum, row in enumerate(coordinates):
    startcolnum = 0
    while startcolnum < len(row):
        if type(row[startcolnum]) == int:
            endcolnum = startcolnum
            while endcolnum + 1 < len(row):
                if type(row[endcolnum + 1]) == int:
                    endcolnum += 1
                else:
                    break
            print(f'Found number on row {rownum}, at {startcolnum}-{endcolnum}')
            result += process(coordinates, rownum, startcolnum, endcolnum)
            startcolnum = endcolnum + 2
        else:
            startcolnum += 1

print(result)
