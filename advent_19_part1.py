
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

class Dummy:
    def __init__(self, name):
        self._name = name
    def __repr__(self):
        return self._name

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
        else:
            condition, target = TRUE, rule
        if target == 'A':
            target = ACCEPT
        if target == 'R':
            target = REJECT
        workflows[wfname].append((condition,target))

for line in s2.strip().splitlines():
    items.append(eval(f'dict({line[1:-1]})'))

def run(wf, item):
    # Return ACCEPT, REJECT, or a worfklow name
    for condition, target in wf:
        if condition is TRUE:
            return target
        assert condition[0] in 'xmas'
        pystring = 'item["' + condition[0] + '"]' + condition[1:]
        #print(f'eval [{pystring}]')
        if eval(pystring):
            #print(f'Going to {target}')
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
