s = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''


class NumberMapper:

    def __init__(self, name):
        self.name = name
        self.maps = list()

    def convert(self, number):
        for m in self.maps:
            if m[1] <= number < m[1] + m[2]:
                return m[0] + (number - m[1])
        return number

    def __str__(self):
        s = f'\n\n{self.name}'
        for tgt, src, size in self.maps:
            s += f'\n  FROM {src}-{src+size-1} TO {tgt}-{tgt+size-1}'
        return s

def process_input(inputstr):

    inputlines = inputstr.splitlines()
    seedstr = inputlines[0].split(':')[1]
    seeds = list(map(int, seedstr.split()))

    maps = list()

    for inputline in inputlines[2:]:
        if inputline == '':
            continue
        if inputline.endswith(' map:'):
            maps.append(NumberMapper(inputline))
            continue
        tgt, src, size = map(int, inputline.strip().split())
        maps[-1].maps.append((tgt, src, size))

    return seeds, maps


from advent_input_05 import s

seeds, maps = process_input(s)

results = list()
for seed in seeds:
    v = seed
    for m in maps:
        v = m.convert(v)
    print(f'{seed} -> {v}')
    results.append(v)

print(min(results))
