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
for output_name in output_names:
    m[output_name] = Output(output_name, list())

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

q = deque()
pulse_counter = {LO:0, HI:0}

for _ in range(1000):
    q.append((m['broadcaster'], LO, None))
    while len(q) > 0:
        component, signal, source = q.popleft()
        pulse_counter[signal] += 1
        result = component.process(signal, source)
        if result is not None:
            q.extend(result)

print(pulse_counter)
print(pulse_counter[LO] * pulse_counter[HI])
