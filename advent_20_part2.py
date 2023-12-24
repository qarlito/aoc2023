import itertools
from collections import deque


s = '''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''

s = '''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''


from advent_input_20 import s


class Dummy:
    def __init__(self, name):
        self._name = name
    def __repr__(self):
        return self._name

HI = Dummy('HI')
LO = Dummy('LO')
OFF = Dummy('OFF')
ON = Dummy('ON')
SUCCESS = Dummy('SUCCESS')

class Component:
    def __init__(self, name, target_names):
        self.name = name
        self.target_names = target_names
    def use_real_targets(self, m):
        self.targets = [m[target_name] for target_name in self.target_names]
    def broadcast(self, signal):
        #for target in self.targets:
        #    print(f'{self.name} -{signal}-> {target.name}')
        return zip(self.targets, itertools.repeat(signal), itertools.repeat(self))

class BroadCaster(Component):
    def process(self, signal, source):
        return self.broadcast(signal)

class FlipFlop(Component):
    def __init__(self, name, target_names):
        super(FlipFlop, self).__init__(name, target_names)
        self.state = OFF
    def process(self, signal, source):
        if signal is LO:
            if self.state is OFF:
                self.state = ON
                return self.broadcast(HI)
            else:
                self.state = OFF
                return self.broadcast(LO)
        else:
            return None

class Conjunction(Component):
    def set_inputs(self, inputs):
        self.input_memory = dict(zip(inputs, itertools.repeat(LO)))
    def process(self, signal, source):
        assert source in self.input_memory
        self.input_memory[source] = signal
        if all(last_signal is HI for last_signal in self.input_memory.values()):
            return self.broadcast(LO)
        else:
            return self.broadcast(HI)

class Output(Component):
    def process(self, signal, source):
        return None

class RX(Component):
    def process(self, signal, source):
        if signal is LO:
            return SUCCESS
        else:
            return None

# Memory
m = dict()

for line in s.strip().splitlines():
    from_, to_ = line.split(' -> ')
    target_names = to_.split(', ')
    if from_ == 'broadcaster':
        assert 'broadcaster' not in m
        m['broadcaster'] = BroadCaster('broadcaster', target_names)
    elif from_[0] == '%':
        name = from_[1:]
        assert name not in m
        m[name] = FlipFlop(name, target_names)
    elif from_[0] == '&':
        name = from_[1:]
        assert name not in m
        m[name] = Conjunction(name, target_names)
    else:
        raise Exception('Impossible')

output_names = set()
for component in m.values():
    for target_name in component.target_names:
        if target_name not in m:
            output_names.add(target_name)
assert len(output_names) == 1
assert output_names == {'rx'}
for output_name in output_names:
    m[output_name] = RX(output_name, list())

for component in m.values():
    component.use_real_targets(m)

for conj in m.values():
    if type(conj) is not Conjunction:
        continue
    inputs = set()
    for component in m.values():
        if conj.name in component.target_names:
            inputs.add(component)
    conj.set_inputs(inputs)


##################################################

for component in m.values():
    s = set(component.targets)
    prev_size = -1
    while len(s) > prev_size:
        prev_size = len(s)
        new_s = set()
        for c in s:
            new_s.add(c)
            new_s.update(c.targets)
        s = new_s
    print(f'{component.name} -> {sorted([c.name for c in s if type(c) == FlipFlop or c.name in ["vt","dq","qt","nl"]])}')
    

for special in ['qt', 'vt', 'nl' ,'dq']:
    print(special, ' has inputs ', [i.name for i in m[special].input_memory.keys()])

#We have the following groups each consisting of 12 flipflops + 1 conjunction
# Broadcaster sends to each of these groups
sgroups = list()
sin = list()
sout = list()
sin.append('kr')
sgroups.append(['cb', 'ch', 'dh', 'hf', 'hh', 'hn', 'kd', 'kq', 'kr', 'lm', 'nb', 'qk', 'vt'])
sout.append('lz')

sin.append('zb')
sgroups.append(['bh', 'bv', 'fr', 'gj', 'gq', 'hm', 'jp', 'qf', 'rb', 'rd', 'sk', 'zb', 'nl'])
sout.append('zm')

sin.append('sm')
sgroups.append(['cf', 'hl', 'hp', 'jv', 'jx', 'nd', 'ng', 'nt', 'rh', 'sl', 'sm', 'vr', 'qt'])
sout.append('pl')

sin.append('xd')
sgroups.append(['fb', 'gx', 'kx', 'lv', 'mh', 'ml', 'mt', 'rc', 'rt', 'ts', 'xd', 'xs', 'dq'])
sout.append('mz')

#  Finally:  (&pl, &mz, &lz, &zm) -> &bn -> rx

def map_group_flipflops_to_number(sgroup):
    # 12 flipflops
    num = 0
    for flipflopname in sgroup[:12]:
        num <<= 1
        if m[flipflopname].state is ON:
            num |= 1
    return num

for GROUP in [0,1,2,3]:
    states_found = {0: 0}   # state -> counter
    q = deque()
    counter = 0
    while True:
        counter += 1
        if counter % 10000 == 0:
            print(counter)
        q.append((m[sin[GROUP]], LO, None))
        while len(q) > 0:
            component, signal, source = q.popleft()
            if component.name == 'bn' and signal is HI:
                print(f'{counter} delivering signal {signal} to bn')
            result = component.process(signal, source)
            if result is not None:
                q.extend(result)
        state = map_group_flipflops_to_number(sgroups[GROUP])
        if state in states_found:
            prev_counter = states_found[state]
            print(f'Been here before! Now={counter}  Prev={prev_counter}  Delta={counter-prev_counter}')
            break


#4003 delivering signal HI to bn
#Been here before! Now=4003  Prev=0  Delta=4003
#3823 delivering signal HI to bn
#Been here before! Now=3823  Prev=0  Delta=3823
#3797 delivering signal HI to bn
#Been here before! Now=3797  Prev=0  Delta=3797
#3881 delivering signal HI to bn
#Been here before! Now=3881  Prev=0  Delta=3881

# math.lcm(4003, 3823, 3797, 3881) equals 225514321828633
