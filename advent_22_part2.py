from collections import defaultdict
import itertools
from copy import deepcopy


s = '''
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
'''

from advent_input_22 import s

X_DIRECTION = 'X'
Y_DIRECTION = 'Y'
Z_DIRECTION = 'Z'

class Block:

    def __init__(self, description):
        from_, to_ = description.split('~')
        fromx, fromy, fromz = [int(c) for c in from_.split(',')]
        tox, toy, toz = [int(c) for c in to_.split(',')]
        self.minx = min(fromx, tox)
        self.maxx = max(fromx, tox)
        self.miny = min(fromy, toy)
        self.maxy = max(fromy, toy)
        self.minz = min(fromz, toz)
        self.maxz = max(fromz, toz)

        if self.minx != self.maxx:
            self.direction = X_DIRECTION
            self.size = self.maxx - self.minx + 1
            assert self.miny == self.maxy
            assert self.minz == self.maxz
        elif self.miny != self.maxy:
            self.direction = Y_DIRECTION
            self.size = self.maxy - self.miny + 1
            assert self.minx == self.maxx
            assert self.minz == self.maxz
        elif self.minz != self.maxz:
            self.direction = Z_DIRECTION
            self.size = self.maxz - self.minz + 1
            assert self.minx == self.maxx
            assert self.miny == self.maxy
        else:
            # 1x1x1 block. Use X direction
            self.direction = X_DIRECTION
            self.size = 1
        self.positions_below = self.get_positions_below()

    def covers(self, position):
        return self.minx<=position[0]<=self.maxx and self.miny<=position[1]<=self.maxy and self.minz<=position[2]<=self.maxz

    def equals(self, otherb):
        return self.minx==otherb.minx and self.miny==otherb.miny and self.minz==otherb.minz and self.direction==otherb.direction and self.size==otherb.size

    def get_positions_below(self):
        if self.direction == Z_DIRECTION:
            return set([(self.minx, self.miny, self.minz-1)])
        elif self.direction == X_DIRECTION:
            return set([(x, self.miny, self.minz-1) for x in range(self.minx, self.maxx+1)])
        else:
            return set([(self.minx, y, self.minz-1) for y in range(self.miny, self.maxy+1)])

    def __str__(self):
        return f'({self.minx}, {self.miny}, {self.minz}) -> ({self.maxx}, {self.maxy}, {self.maxz})   [{self.direction} size={self.size}]'


class Structure:

    def __init__(self, blocks):
        self.hor = defaultdict(lambda: set())         # { z : {block1, block2, ...} }  # Directions X and Y
        self.ver_min = defaultdict(lambda: set())     # { z : {block1, block2, ...} }  # Direction Z. Block minz
        self.ver_max = defaultdict(lambda: set())     # { z : {block1, block2, ...} }  # Direction Z. Block maxz

        for b in blocks:
            if b.direction in [X_DIRECTION, Y_DIRECTION]:
                self.hor[b.minz].add(b)
            else:
                self.ver_min[b.minz].add(b)
                self.ver_max[b.maxz].add(b)

    def copy(self):
        return deepcopy(self)

    def get_range(self):
        globalminz = min(itertools.chain(self.hor.keys(), self.ver_min.keys()))
        globalmaxz = max(itertools.chain(self.hor.keys(), self.ver_max.keys()))
        return globalminz, globalmaxz

    def is_covered(self, position, skip_block=None):
        if position[2] in self.hor:
            for block in self.hor[position[2]]:
                if block is not skip_block and block.covers(position):
                    return True
        if position[2] in self.ver_max:
            for block in self.ver_max[position[2]]:
                if block is not skip_block and block.covers(position):
                    return True
        return False

    def falldown(self, b, simulate=False, skip_block=None):
        is_hor = b.minz in self.hor and b in self.hor[b.minz]
        is_ver = b.minz in self.ver_min and b in self.ver_min[b.minz]
        assert is_hor or is_ver

        new_minz = 1
        pos_below = b.get_positions_below()
        for z in range(b.minz-1, 0, -1):
            for pos in pos_below:
                if self.is_covered((pos[0], pos[1], z), skip_block):
                    new_minz = z + 1
                    break
            if new_minz != 1:
                break

        if simulate:
            return new_minz < b.minz

        if new_minz < b.minz:
            #print(f'{"Hor" if is_hor else "Ver"} Block {b} is falling down from {b.minz} to {new_minz}')
            if is_hor:
                self.hor[b.minz].remove(b)
                if not self.hor[b.minz]:
                    del self.hor[b.minz]
                b.minz = new_minz
                b.maxz = new_minz
                self.hor[new_minz].add(b)
            else:
                self.ver_min[b.minz].remove(b)
                if not self.ver_min[b.minz]:
                    del self.ver_min[b.minz]
                self.ver_max[b.maxz].remove(b)
                if not self.ver_max[b.maxz]:
                    del self.ver_max[b.maxz]
                b.minz = new_minz
                b.maxz = b.minz + b.size - 1
                self.ver_min[b.minz].add(b)
                self.ver_max[b.maxz].add(b)
            # Falling
            return True
        else:
            # Not falling
            return False

    def __str__(self):
        globalminz, globalmaxz = self.get_range()
        s = [f'Structure from z={globalminz} -> z={globalmaxz}']
        for z in range(globalminz, globalmaxz + 1):
            if z in self.hor:
                for b in self.hor[z]:
                    s.append(str(b))
            if z in self.ver_min:
                for b in self.ver_min[z]:
                    s.append(str(b))
        return '\n'.join(s)


d = Structure({Block(line.strip()) for line in s.strip().splitlines()})

print(d)
print()
print(f'hor keys: {d.hor.keys()}')
print(f'range:    {d.get_range()}')
print()

globalminz, globalmaxz = d.get_range()
for z in range(globalminz, globalmaxz + 1):
    if z in d.hor:
        for b in d.hor[z].copy():
            d.falldown(b)
    if z in d.ver_min:
        for b in d.ver_min[z].copy():
            d.falldown(b)

print()
print(d)
print()
print(f'hor keys: {d.hor.keys()}')
print(f'range:    {d.get_range()}')



def count_num_falling_blocks_when_removing(orig_d, orig_removed_block):
    d = deepcopy(orig_d)
    removed_block = None
    # First find the deepcopy of orig_removed_block
    if orig_removed_block.direction is Z_DIRECTION:
        assert orig_removed_block.minz in d.ver_min
        for b in d.ver_min[orig_removed_block.minz]:
            if orig_removed_block.equals(b):
                removed_block = b
                break
    else:
        assert orig_removed_block.minz in d.hor
        for b in d.hor[orig_removed_block.minz]:
            if orig_removed_block.equals(b):
                removed_block = b
                break
    assert removed_block is not None
    
    # Now let the blocks fall
    counter = 0 
    globalminz, globalmaxz = d.get_range()
    for z in range(removed_block.minz+1, globalmaxz + 1):
        if z in d.hor:
            for b in d.hor[z].copy():
                if b is not removed_block:
                    if d.falldown(b, False, removed_block):
                        counter += 1
        if z in d.ver_min:
            for b in d.ver_min[z].copy():
                if b is not removed_block:
                    if d.falldown(b, False, removed_block):
                        counter += 1
    return counter

total = 0
globalminz, globalmaxz = d.get_range()
for z in range(globalminz, globalmaxz + 1):
    if z in d.hor:
        for b in d.hor[z]:
            total += count_num_falling_blocks_when_removing(d, b)
    if z in d.ver_min:
        for b in d.ver_min[z]:
            total += count_num_falling_blocks_when_removing(d, b)
    print(f'Finished z={z} -> total={total}')
print(f'TOTAL {total}')
