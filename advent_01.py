number_numbers = list(map(str, range(10)))
number_strings = ['one', 'two', 'three', 'four', 'five' ,'six', 'seven', 'eight', 'nine']
backwards_number_strings = [s[::-1] for s in number_strings]

forward_map = dict(zip(number_numbers, range(10)))
forward_map.update(dict(zip(number_strings, range(1,10))))

backward_map = dict(zip(number_numbers, range(10)))
backward_map.update(dict(zip(backwards_number_strings, range(1,10))))

def get_first_offset(line, number_map):
    for i in range(len(line)):
        for number_str, number_value in number_map.items():
            if line[i:].startswith(number_str):
                return i, number_value
    raise Exception(f'Error: {line}')


def process_line(line):
    first_offset, first_value = get_first_offset(line, forward_map)
    last_offset, last_value = get_first_offset(line[::-1], backward_map)
    #print (first_offset, first_value, last_offset, last_value)
    return first_value*10 + last_value


s = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''

from advent_input_01 import s

print(sum([process_line(line) for line in s.splitlines()]))

