s = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''

from advent_input_09 import s


# Gather input

numbers = list()
for line in s.strip().splitlines():
    row = [x for x in map(int, line.strip().split())]
    # part 2 -> just reverse the input rows
    row.reverse()
    numbers.append(row)
#print(numbers)


def is_all_zeroes(row):
    return all([i==0 for i in row])


def puzzle(inputrow):
    success = False
    m = [inputrow]
    for depth in range(len(m[0])):
        current_row = m[depth]
        if is_all_zeroes(current_row):
            success = True
            break
        new_row = [x[1]-x[0] for x in zip(current_row[:-1], current_row[1:])]
        m.append(new_row)
    if not success:
        raise Exception('No all-zero row found!')
    m[-1].append(0)
    for depth in range(len(m)-2, -1, -1):
        m[depth].append(m[depth+1][-1] + m[depth][-1])
    print(m)
    return m[0][-1]


total = 0
for inputrow in numbers:
    print('----')
    print(inputrow)
    result = puzzle(inputrow)
    print(f'puzzle {[i for i in inputrow]} -> {result}')
    total += result

print(f'TOTAL: {total}')
