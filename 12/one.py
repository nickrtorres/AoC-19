import collections
import re

raw = '''\
<x=-17, y=9, z=-5>
<x=-1, y=7, z=13>
<x=-19, y=12, z=5>
<x=-6, y=-6, z=-4>
'''

class Moon:
    def __init__(self, s):
        x, y, z = re.match(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', s).groups()
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.dx, self.dy, self.dz = 0, 0, 0
        self.neighbors = []

    def total_energy(self):
        return self._potential_energy() * self._kinetic_energy()
    '''
    A moon's potential energy is the sum of the absolute values of its x, y, and z position coordinates
    '''
    def _potential_energy(self):
        return sum((abs(self.x), abs(self.y), abs(self.z)))

    '''
    A moon's kinetic energy is the sum of the absolute values of its velocity coordinates
    '''
    def _kinetic_energy(self):
        return sum((abs(self.dx), abs(self.dy), abs(self.dz)))

    def add_neighbors(self, neighbors):
        self.neighbors = [n for n in neighbors if n != self]

    def update_position(self):
        self.x, self.y, self.z = self.x + self.dx, self.y + self.dy, self.z + self.dz

    def update_velocity(self):
        for neighbor in self.neighbors:
            if self.x < neighbor.x:
                self.dx = self.dx + 1
            elif self.x > neighbor.x:
                self.dx = self.dx - 1

            if self.y < neighbor.y:
                self.dy = self.dy + 1
            elif self.y > neighbor.y:
                self.dy = self.dy - 1

            if self.z < neighbor.z:
                self.dz = self.dz + 1
            elif self.z > neighbor.z:
                self.dz = self.dz - 1

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.dx, self.dy, self.dz))

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y and other.z == self.z

    def __str__(self):
        return f'pos=<x={self.x}, y={self.y}, z={self.z}>, vel=<x={self.dx}, y={self.dy}, z={self.dz}>'


moons = []
for line in raw.splitlines():
    moons.append(Moon(line))

for moon in moons:
    moon.add_neighbors(moons)

def p(moons):
    for moon in moons:
        print(str(moon))

def step(moons):
    for moon in moons:
        moon.update_velocity()

    for moon in moons:
        moon.update_position()

universes = set()
for s in range(10000000000000):
    print(s)
    universe = tuple(moons)
    if universe in universes:
        print(s)
        break
    else:
        universes.add(universe)
    step(moons)



print(sum(m.total_energy() for m in moons))
