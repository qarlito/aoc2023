

def to_coordinates(inputstr):
    result = list()
    for row in inputstr.splitlines():
        rowlist = list()
        result.append(rowlist)
        for symbol in row:
            if symbol.isdigit():
                rowlist.append(int(symbol))
            elif symbol == '*':
                rowlist.append('*')
            else:
                rowlist.append('.')
    return result


def is_gear(coordinates, row, col):
    if row<0 or row>=len(coordinates):
        return False
    if col<0 or col>=len(coordinates[0]):
        return False
    return coordinates[row][col] == '*'


def get_touching_gears(coordinates, row_number, start_pos, end_pos):
    gear_coordinates = list()
    for row in range(row_number-1, row_number+2):
        for col in range(start_pos-1, end_pos+2):
            if is_gear(coordinates, row, col):
                gear_coordinates.append((row, col))
    return gear_coordinates


def process(coordinates, row_number, start_pos, end_pos, gear_registry):
    number_value = int(''.join(map(str, coordinates[row_number][start_pos:end_pos+1])))
    gear_coordinates = get_touching_gears(coordinates, row_number, start_pos, end_pos)
    print(number_value, gear_coordinates)
    for gear_coordinate in gear_coordinates:
        touching_numbers_for_gear = gear_registry.get(gear_coordinate, list())
        touching_numbers_for_gear.append((row_number, start_pos, number_value))
        gear_registry[gear_coordinate] = touching_numbers_for_gear


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
gear_registry = dict()

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
            process(coordinates, rownum, startcolnum, endcolnum, gear_registry)
            startcolnum = endcolnum + 2
        else:
            startcolnum += 1

result = 0
for gear_coordinate, touching_numbers in gear_registry.items():
    if len(touching_numbers) == 2:
        result += touching_numbers[0][2] * touching_numbers[1][2]

print(result)
