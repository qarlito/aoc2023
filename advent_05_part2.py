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


class Convertor:

    def __init__(self, start, end, delta):
        self.start = start
        self.end = end
        self.delta = delta

    def __str__(self):
        return f'Range {self.start}-{self.end} with delta {self.delta} - new start is {self.start+self.delta}'


class NumberRange:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def send_through_convertor(self, convertor):
        # Returns a list of NumberRanges that are not processed by this convertor (0, 1, or 2)
        # Plus a list of NumberRanges that are processed (0 or 1)

        sub_ranges = list()
        converted_ranges = list()

        if self.end < convertor.start or self.start > convertor.end:
            # No overlap
            sub_ranges.append(self)
        else:
            if (convertor.start > self.start):
                # Keep left part for further processing
                sub_ranges.append(NumberRange(self.start, convertor.start - 1))
            if (convertor.end < self.end):
                # Keep right part for further processing
                sub_ranges.append(NumberRange(convertor.end + 1, self.end))
            # Convert part
            converted_ranges.append(NumberRange(max(self.start, convertor.start) + convertor.delta, min(self.end, convertor.end) + convertor.delta))

        print(f'    Convertor {convertor} processed {self}')
        print(f'       KEEP: {ranges_to_string(sub_ranges)}')
        print(f'       CONV: {ranges_to_string(converted_ranges)}')
        return sub_ranges, converted_ranges

    def __str__(self):
        return f'Range {self.start}-{self.end}'


def process_input(inputstr):
    inputlines = inputstr.splitlines()
    seedstr = inputlines[0].split(':')[1]
    seed_ranges = list(map(int, seedstr.split()))
    seeds = list()
    for i in range(len(seed_ranges)//2):
        seeds.append(NumberRange(seed_ranges[2*i], seed_ranges[2*i]+seed_ranges[2*i+1]-1))

    maps = list()

    for inputline in inputlines[2:]:
        if inputline == '':
            continue
        if inputline.endswith(' map:'):
            maps.append(list())
            continue
        tgt, src, size = map(int, inputline.strip().split())
        maps[-1].append(Convertor(src, src+size-1, tgt-src))

    return seeds, maps


def ranges_to_string(ranges):
    v = ''
    for r in ranges:
        v = v + f'{r.start}-{r.end} '
    return v


from advent_input_05 import s

seeds, maps = process_input(s)

input_ranges = [r for r in seeds]
print('START')
print('  ' + ranges_to_string(input_ranges))
for m in maps:
    processed_ranges = list() # already processed by this map
    print('APPLYING MAP')
    for x in m:
        print(f'  {x} - target start is {x.start + x.delta}')
    for convertor in m:
        # transform
        finer_input_ranges = list()     # Refinements of input_ranges
        for r in input_ranges:
            sub_ranges, converted_ranges = r.send_through_convertor(convertor)
            finer_input_ranges.extend(sub_ranges)
            processed_ranges.extend(converted_ranges)
        input_ranges = finer_input_ranges
    processed_ranges.extend(finer_input_ranges) # If any range was not converted by this map, just keep it unmodified
    input_ranges = processed_ranges
    input_ranges.sort(key=lambda r: r.start)
    print('RESULT')
    print('  ' + ranges_to_string(input_ranges))

print([str(x) for x in input_ranges])

print('MINIMUM IS:', min([x.start for x in input_ranges]))
