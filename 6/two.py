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


def count_value(o, cur, target=''):
    try:
        if o[cur] == target:
            return 0
        next = o[cur]
        return 1 + count_value(o, next, target)
    except KeyError:
        return 0


def get_ancestors(o, cur):
    try:
        return  [o[cur]] + list(get_ancestors(o, o[cur]))
    except KeyError:
        return []

assert 2 == count_value(orbits, 'C')
assert 5 == count_value(orbits, 'F')
assert 7 == count_value(orbits, 'L')
assert 42 == sum(count_value(orbits, c) for c in orbits.keys())


def find_common_ancestor(orbits, p1, p2):
    p1_ancestors = get_ancestors(orbits, p1)
    p2_ancestors = get_ancestors(orbits, p2)

    for p1A in p1_ancestors:
        for p2A in p2_ancestors:
            if p1A == p2A:
                return p1A
    return None

assert 0 == count_value(orbits, 'I', 'D')
assert 2 == count_value(orbits, 'K', 'D')


def orbital_transfers(orbits, p1, p2):
    ancestor = find_common_ancestor(orbits, p1, p2)

    return count_value(orbits, p1, ancestor) + count_value(orbits, p2, ancestor)

assert 2 == orbital_transfers(orbits, 'K', 'I')


with open('input') as f:
    puzzle = f.read()
orbits = get_orbits(puzzle)
print(orbital_transfers(orbits, 'YOU', 'SAN'))

