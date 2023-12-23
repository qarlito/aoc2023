
s = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''


from advent_input_19 import s

DIMENSIONS = {'x':0, 'm':1, 'a':2, 's':3}

class Dummy:
    def __init__(self, name):
        self._name = name
    def __repr__(self):
        return self._name

EMPTYCUBE = Dummy('EmptyCube')
LEFT = Dummy('left')
RIGHT = Dummy('right')

class XMASCube:

    # E.g. cube = XMASCube([(1,4000), (10,4000), (10,3000), (100,100)])
    # That are the inclusive boundaries of the 4 dimensions x,m,a,s
    def __init__(self, ranges):
        assert len(ranges) == 4
        for min_, max_ in ranges:
            assert min_ <= max_
        self._ranges = ranges

    def __str__(self):
        s = ''
        for dim in 'xmas':
            s += f'{dim}[{self._ranges[DIMENSIONS[dim]][0]} - {self._ranges[DIMENSIONS[dim]][1]}]  '
        s += f'(vol={self.volume()})'
        return s

    def volume(self):
        result = 1
        for min_, max_ in self._ranges:
            result *= (max_ - min_ + 1)
        return result

    # Return overlapping_cube, remaining_cube
    def cut(self, dimension, exclusive_boundary, overlapping_direction):
        mymin, mymax = self._ranges[DIMENSIONS[dimension]]
        if overlapping_direction == LEFT:
            min_ = mymin
            max_ = exclusive_boundary - 1
        elif overlapping_direction == RIGHT:
            min_ = exclusive_boundary + 1
            max_ = mymax
        else:
            raise Exception('Impossible')
        
        if mymin > max_ or mymax < min_:
            # No overlap
            return EMPTYCUBE, self
        else:
            overlapping_range = (max(min_, mymin), min(max_, mymax))
            overlapping_ranges = self._ranges.copy()
            overlapping_ranges[DIMENSIONS[dimension]] = overlapping_range
            overlapping_cube = XMASCube(overlapping_ranges)

            if max_ < mymax:
                nonoverlapping_range = (max_+1, mymax)
            elif mymin < min_:
                nonoverlapping_range = (mymin, min_-1)
            else:
                nonoverlapping_range = None
 
            if nonoverlapping_range is None:
                nonoverlapping_cube = EMPTYCUBE
            else:
                nonoverlapping_ranges = self._ranges.copy()
                nonoverlapping_ranges[DIMENSIONS[dimension]] = nonoverlapping_range
                nonoverlapping_cube = XMASCube(nonoverlapping_ranges)

            return overlapping_cube, nonoverlapping_cube


TRUE = Dummy('<True>')
ACCEPT = Dummy('<A>')
REJECT = Dummy('<R>')
workflows = dict()
items = list()

s1, s2 = s.strip().split('\n\n')
for line in s1.strip().splitlines():
    wfname, descr = line[:-1].split('{')
    workflows[wfname] = list()
    for rule in descr.split(','):
        if ':' in rule:
            condition, target = rule.split(':')
            assert condition[0] in 'xmas'
            assert condition[1] in '<>'
            condition = (condition[0], int(condition[2:]), LEFT if condition[1]=='<' else RIGHT)
        else:
            condition, target = TRUE, rule
        if target == 'A':
            target = ACCEPT
        if target == 'R':
            target = REJECT
        workflows[wfname].append((condition,target))

from pprint import pprint
pprint(workflows)

for line in s2.strip().splitlines():
    items.append(eval(f'dict({line[1:-1]})'))

def run(wf, item):
    # Return ACCEPT, REJECT, or a worfklow name
    for condition, target in wf:
        if condition is TRUE:
            return target

        if condition[2] is LEFT:
            bool_result = item[condition[0]] < condition[1]
        else:
            bool_result = item[condition[0]] > condition[1]

        if bool_result:
            return target
    raise Exception('Impossible')

total = 0
for item in items:
    #print(f'\nProcessing item {item}')
    wfname = 'in'
    while True:
        #print(f'Running workflow {wfname}')
        result = run(workflows[wfname], item)
        if result in {ACCEPT, REJECT}:
            break
        wfname = result
    print(f'item {item} -> {result}')
    if result == ACCEPT:
        total += sum(item.values())

print(f'TOTAL {total}')


cube = XMASCube([(1,4000), (1,4000), (1,4000), (1,4000)])
to_be_processed = {(cube, 'in')}
total = 0

while len(to_be_processed) > 0:
    output = set()
    while len(to_be_processed) > 0:
        (cube, wfname) = to_be_processed.pop()
        if wfname is ACCEPT:
            print('Survivor: ' + str(cube))
            total += cube.volume()
            continue
        elif wfname is REJECT:
            continue
        else:
            wf = workflows[wfname]
            for condition, target in wf:
                if condition is TRUE:
                    output.add((cube, target))
                    break
                else:
                    overlapping_cube, nonoverlapping_cube = cube.cut(condition[0], condition[1], condition[2])
                    if overlapping_cube is not EMPTYCUBE:
                        output.add((overlapping_cube, target))
                    if nonoverlapping_cube is EMPTYCUBE:
                        break
                    cube = nonoverlapping_cube
    to_be_processed = output


print(f'TOTAL: {total}')





