# Exact matrix calculation (with integers or fractions or symbols)
from sympy.matrices import Matrix


'''

Let px,py,pz be start pos
Let vx,vy,vz be start speed

Let PXi,PYi,PZi be the start pos of hailstone i
Let VXi,VYi,VZi be the start speed of hailstone i



Collision at time t1 with hailstone 1. Can be writen as:

PX1 + VX1 * t1 = px + vx * t1
==> (vx - VX1) * t1 = (PX1 - px)



Now warite this for both x and y and manipulate the equation

(vx - VX1) * t1 = (PX1 - px)
(vy - VY1) * t1 = (PY1 - py)

[[ Assume/guess t is not zero ]]
(PX1 - px) * (vy - VY1)  = (PY1 - py) * (vx - VX1) 

PX1.vy + VY1.px - PX1.VY1 - px.vy = PY1.vx + VX1.py - PY1.VX1 + py.vx


Write down collisions with hailstone 1 and 2 and further manipulate the equation

PX1.vy + VY1.px - PX1.VY1 - px.vy = PY1.vx + VX1.py - PY1.VX1 + py.vx
PX2.vy + VY2.px - PX2.VY2 - px.vy = PY2.vx + VX2.py - PY2.VX2 + py.vx

(PX1-PX2).vy + (VY1-VY2).px - PX1.VY1 + PX2.VY2
   =  (PY1-PY2).vx + (VX1-VX2).py - PY1.VX1 + PY2.VX2

(VY1-VY2).px - (VX1-VX2).py  - (PY1-PY2).vx + (PX1-PX2).vy
   =  PX1.VY1 - PX2.VY2 - PY1.VX1 + PY2.VX2


We end up with a linear equation in px, py, vx, vy.
We can write such an equation for every pair of hailstones.

Let's use exact math (sympy) and work with the hailstone pairs
(1,2)  (1,3)  (1,4)  (1,5)

In theory we should check for all gropus of 5 hailstones in the inputset.
'''



s = '''
19, 13, 30 @ -2, 1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @ 1, -5, -3
'''

from advent_input_24 import s

data = list()
for line in s.strip().splitlines():
    p, v = line.strip().split(' @ ')
    px, py, pz = [int(c) for c in p.split(', ')]
    vx, vy, vz = [int(c) for c in v.split(', ')]
    data.append(((px, py, pz), (vx, vy, vz)))


def solve(START=0):
    A = list()
    B = list()
    C = list()
    D = list()

    (px1, py1, pz1), (vx1, vy1, vz1) = data[START]
    for (px2, py2, pz2), (vx2, vy2, vz2) in data[START+1:START+5]:
        A.append([vy1-vy2, -(vx1-vx2), -(py1-py2), px1-px2])
        B.append([px1*vy1 - px2*vy2 - py1*vx1 + py2*vx2])
        C.append([vz1-vz2, -(vx1-vx2), -(pz1-pz2), px1-px2])
        D.append([px1*vz1 - px2*vz2 - pz1*vx1 + pz2*vx2])

    print('\nSolving for px, py, vx, vy')
    a = Matrix(A)
    b = Matrix(B)
    xy = a.solve(b)
    print(xy)

    print('\nSolving for px, pz, vx, vz')
    c = Matrix(C)
    d = Matrix(D)
    xz = c.solve(d)
    print(xz)

    assert xy[0] == xz[0]
    assert xy[2] == xz[2]
    result = xy[0] + xy[1] + xz[1]
    return result


print('\nSUM is', solve(0))
