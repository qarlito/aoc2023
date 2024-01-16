import sys
from pprint import pprint

s = '''
19, 13, 30 @ -2, 1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @ 1, -5, -3
'''

BOX_X = [7, 27]
BOX_Y = [7, 27]


from advent_input_24 import s
BOX_X = [200000000000000, 400000000000000]
BOX_Y = [200000000000000, 400000000000000]


d = list()
for line in s.strip().splitlines():
    p, v = line.strip().split(' @ ')
    px, py, pz = [int(c) for c in p.split(', ')]
    vx, vy, vz = [int(c) for c in v.split(', ')]
    d.append(((px, py, pz), (vx, vy, vz)))




num_crossing = 0

for i, ((pxa, pya, pza), (vxa, vya, vza)) in enumerate(d):
    for ((pxb, pyb, pzb), (vxb, vyb, vzb)) in d[i+1:]:
        print(f'\nChecking {((pxa, pya, pza), (vxa, vya, vza))} and {((pxb, pyb, pzb), (vxb, vyb, vzb))}')
        det = - vxa * vyb + vxb * vya
        if det == 0:
            print(f'Parallel')
        else:
            ta = (vyb * (pxa - pxb) - vxb * (pya - pyb)) / det
            tb = (vya * (pxa - pxb) - vxa * (pya - pyb)) / det
            if (ta<0) or (tb<0):
                print(f'Negative time')
                continue
            x = pxa + vxa * ta
            y = pya + vya * ta
            if BOX_X[0] <= x <= BOX_X[1] and BOX_Y[0] <= y <= BOX_Y[1]:
                num_crossing += 1
                print(f'Collision in box ({x},{y})')
            else:
                print(f'No collision in box')

print(f'\n\nTOTAL: {num_crossing}')
