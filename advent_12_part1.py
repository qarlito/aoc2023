s = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''


FINISHED = 'FINISHED'
FAILURE  = 'FAILURE'
SUCCESS  = 'SUCCESS'


def extend_location(springs, seq_lens, positions, start=0):

    num_positions= len(positions)

    if len(seq_lens) == num_positions:
        if '#' in springs[positions[num_positions-1] + seq_lens[num_positions-1]:]:
            return FAILURE
        else:
            return FINISHED

    if start >= len(springs):
        return FAILURE

    # Should skip no springs
    if num_positions > 0:
        start = max(start, positions[num_positions-1] + seq_lens[num_positions-1] + 1)
    leading_void_beginning = 0
    if num_positions > 0:
        leading_void_beginning = positions[-1] + seq_lens[num_positions-1]
    if '#' in springs[leading_void_beginning:start]:
        return FAILURE

    seq_len = seq_lens[num_positions]
    while start + seq_len <= len(springs):
        if '.' not in springs[start:start+seq_len]:
            if start + seq_len == len(springs) or springs[start + seq_len] in '.?':
                positions.append(start)
                return SUCCESS
        if springs[start] == '#':
            # Cannot jump over a '#'
            break
        start += 1
    return FAILURE

def print_solution(springs, seq_lens, positions):
    assert len(seq_lens) == len(positions)
    result = '.' * positions[0]
    for n in range(len(positions)-1):
        result += '#' * seq_lens[n]
        result += '.' * (positions[n+1] - positions[n] - seq_lens[n])
    result += '#' * seq_lens[-1]
    result += '.' * (len(springs) - positions[-1] - seq_lens[-1])
    assert len(result) == len(springs)
    print(result)


def solve_puzzle(springs, seq_lens):
    offset = 0
    positions = []
    success_count = 0
    while True:
        result = extend_location(springs, seq_lens, positions, offset)
        num_positions = len(positions)
        if result == SUCCESS:
            offset = positions[num_positions-1] + seq_lens[num_positions-1] + 1
        elif result == FINISHED:
            print_solution(springs, seq_lens, positions)
            success_count += 1
            offset = positions.pop() + 1
        elif result == FAILURE:
            if len(positions) == 0:
                # We are finished
                break
            offset = positions.pop() + 1
    return success_count


from advent_input_12 import s

#s = '????.?#???##?#??. 1,1,6'
#s = '??#.#?#.??????### 3,3,1,3'
#s = '?.# 1'

all_springs = list()
all_seq_lens = list()
for line in s.splitlines():
    springs, seqstr = line.split()
    seq_lens = [int(i) for i in seqstr.split(',')]
    all_springs.append(springs)
    all_seq_lens.append(seq_lens)

total = 0
for PUZZLE in range(len(all_springs)):
    springs = all_springs[PUZZLE]
    seq_lens = all_seq_lens[PUZZLE]
    print(springs, seq_lens)
    success_count = solve_puzzle(springs, seq_lens)
    print(f'   -> {success_count}')
    print()
    total += success_count

print(f'TOTAL: {total}')
