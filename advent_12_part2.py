s = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''


def get_solution_str(springs, seq_lens, positions):
    num_positions = len(positions)
    if num_positions == 0:
        return '.' * len(springs)
    result = '.' * positions[0]
    for n in range(len(positions)-1):
        result += '#' * seq_lens[n]
        result += '.' * (positions[n+1] - positions[n] - seq_lens[n])
    result += '#' * seq_lens[num_positions-1]
    result += '.' * (len(springs) - positions[num_positions-1] - seq_lens[num_positions-1])
    assert len(result) == len(springs)
    return result


from advent_input_12 import s

#s = '''.??..??...?##. 1,1,3'''
#s = '''???.### 1,1,3'''
#s = '''?###?#??. 5'''

MULTIPLIER = 5

all_springs = list()
all_seq_lens = list()
for line in s.splitlines():
    springs, seqstr = line.split()
    springs = '?'.join([springs]*MULTIPLIER)
    seqstr = ','.join([seqstr]*MULTIPLIER)
    seq_lens = [int(i) for i in seqstr.split(',')]
    all_springs.append(springs)
    all_seq_lens.append(seq_lens)


def find_first_non_dot(springs):
    first_spring = springs.find('#')
    first_qm = springs.find('?')
    if first_spring != -1:
        if first_qm != -1:
            return min(first_spring, first_qm)
        else:
            return first_spring
    if first_qm != -1:
        return first_qm
    return -1


def solve_puzzle(springs, seq_lens, cache):
    #print(f'  SOLVING {springs} / {seq_lens}')
    cache_key = (len(springs), len(seq_lens))
    if cache_key in cache:
        return cache[cache_key]

    seq_len = seq_lens[0]
    first_spring = springs.find('#')
    end_non_incl = len(springs) if first_spring == -1 else first_spring+1
    end_non_incl = min(end_non_incl, len(springs)-seq_len+1)
    result_count = 0

    first_start = find_first_non_dot(springs)
    if first_start != -1:
        #print(f'Trying range {first_start}-{end_non_incl}')
        for start in range(first_start, end_non_incl):
            assert '#' not in springs[0:start]
            if '.' in springs[start:start+seq_len]:
                continue
            if len(seq_lens) == 1:
                if '#' in springs[start+seq_len:]:
                    continue
                else:
                    result_count += 1
            else:
                # Recurse
                if '#' in springs[start+seq_len:start+seq_len+1]:
                    continue
                else:
                    new_start = find_first_non_dot(springs[start + seq_len + 1:])
                    if new_start != -1:
                        result_count += solve_puzzle(springs[start + seq_len + 1 + new_start:], seq_lens[1:], cache)
                    else:
                        pass
    #print(f'    RESULT for {springs} / {seq_lens} is {result_count}')
    cache[cache_key] = result_count
    return result_count


total = 0
for puzzle_num in range(len(all_springs)):
     springs = all_springs[puzzle_num]
     seq_lens = all_seq_lens[puzzle_num]
     cache = dict()
     #print(f'PUZZLE {springs} - {seq_lens}')
     result = solve_puzzle(springs, seq_lens, cache)
     #print(f'PUZZLE {springs} - {seq_lens} - result={result}\n')
     total += result


print(f'TOTAL: {total}')
