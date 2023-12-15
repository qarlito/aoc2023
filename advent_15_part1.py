
s = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''

from advent_input_15 import s

def hash(input_str):
    result = 0
    for c in input_str:
        result += ord(c)
        result *= 17
        result = result & 0xff
    return result


total = 0
for part in s.split(','):
    h = hash(part)
    print(f'{part} => {h}')
    total += h

print(f'TOTAL {total}')
