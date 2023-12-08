s = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''

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
ILEN = len(instructions)
print(f'Instruction lenght = {ILEN}')

def find_first_trailing_z(start_node, instructions, path, start_counter=0):
    node = start_node
    counter = start_counter
    offset = start_counter % len(instructions)
    print(f'Starting node {node} (steps={start_counter} already done)')
    while True:
        for instruction in instructions[offset:]:
            offset = 0
            counter += 1
            if instruction == 'L':
                node = path[node][0]
            else:
                node = path[node][1]
            if node[2] == 'Z':
                return node, counter

factors = list()
for src_node in path.keys():
    if src_node[2] == 'A':
        print(f'---- {src_node} ----')
        target_node, counter = find_first_trailing_z(src_node, instructions, path)
        print(f'{src_node} -> {target_node} in {counter} steps')
        
        target_node_2, counter_2 = find_first_trailing_z(target_node, instructions, path, 0)
        print(f'{target_node} -> {target_node_2} in {counter} steps')

        # The following is an extreme coincidence
        assert target_node_2 == target_node
        assert counter_2 == counter
        assert counter % ILEN == 0

        factors.append(counter // ILEN)

import math
print()
print('Least common multiple:')
print(math.lcm(*factors) * ILEN)
