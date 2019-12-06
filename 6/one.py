import re

input = '''\
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
'''


def get_orbits(input):
    orbits = {}
    for line in input.splitlines():
        (one, two) = re.match(r'([A-Z0-9]+)\)([A-Z0-9]+)', line).groups()
        orbits[two] = one
    return orbits

orbits = get_orbits(input)


def count_value(o, cur):
    try:
        return 1 + count_value(o, o[cur])
    except KeyError:
        return 0

assert 2 == count_value(orbits, 'C')
assert 5 == count_value(orbits, 'F')
assert 7 == count_value(orbits, 'L')

assert 42 == sum(count_value(orbits, c) for c in orbits.keys())


with open('input') as f:
    puzzle = f.read()

orbits = get_orbits(puzzle)
print(sum(count_value(orbits, c) for c in orbits.keys()))
