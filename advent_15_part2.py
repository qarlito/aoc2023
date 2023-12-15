
s = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''

from advent_input_15 import s

def hash(input_str):
    result = 0
    for c in input_str:
        result += ord(c)
        result *= 17
        result = result & 0xff
    return result


boxes = dict()
for b in range(256):
    boxes[b] = list()
lens_info = dict()

total = 0
for part in s.split(','):
    dash_offset = part.find('-')
    eq_offset = part.find('=')
    if dash_offset != -1:
        # remove a lens
        assert dash_offset == len(part)-1
        lens = part[:-1]
        if lens in lens_info:
            box, _ = lens_info.pop(lens)
            print(f'Pop {lens} from box {box}')
            boxes[box].remove(lens)
    else:
        assert eq_offset != -1
        focus = int(part[eq_offset+1:])
        lens = part[:eq_offset]
        if lens in lens_info:
            box, _ = lens_info[lens]
            lens_info[lens] = box, focus
            assert lens in boxes[box]
        else:
            box = hash(lens)
            boxes[box].append(lens)
            lens_info[lens] = box, focus

total = 0

for lens, (box, focus) in lens_info.items():
    result = (box+1) * (boxes[box].index(lens)+1) * (focus)
    print(f'lens {lens} => {result}')
    total += result

print(f'TOTAL {total}')
