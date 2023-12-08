s = '''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''


from advent_input_08 import s


def read_input(inputstr):
    lines = inputstr.splitlines()
    instructions = lines[0].strip()
    path = dict()
    for line in lines[2:]:
        src, targets = line.split(' = ')
        target_left, target_right = targets[1:-1].split(', ')
        path[src.strip()] = (target_left.strip(), target_right.strip())
    return instructions, path


instructions, path = read_input(s)

def count_steps(instructions, path):
    node = 'AAA'
    counter = 0
    print(f'Starting node {node}')
    while True:
        for instruction in instructions:
            if node == 'ZZZ':
                return counter
            counter += 1
            if instruction == 'L':
                node = path[node][0]
                if (counter % 10000 == 0):
                    print(f'{counter} Going  left to {node}')
            else:
                node = path[node][1]
                if (counter % 10000 == 0):
                    print(f'{counter} Going right to {node}')

print(f'\nTotal steps: {count_steps(instructions, path)}')
