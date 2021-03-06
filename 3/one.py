import re

directions = {
    'R' : lambda x, y, delta: ((x + delta, y), [(dx, y) for dx in range(x, x + delta)]),
    'L' : lambda x, y, delta: ((x - delta, y), [(dx, y) for dx in range(x, x - delta, -1)]),
    'D' : lambda x, y, delta: ((x, y - delta), [(x, dy) for dy in range(y, y - delta, -1)]),
    'U' : lambda x, y, delta: ((x, y + delta), [(x, dy) for dy in range(y, y + delta)]),
}


def parse(input):
    return (re.match(r'([RLDU])([0-9]+)', instruction).groups() for instruction in input.split(','))


def get_points(input):
    points = set()
    x, y = (0, 0)
    for (dir, delta) in parse(input):
        ((x, y), visited) = directions[dir](int(x), int(y), int(delta))
        points |= set(visited)

    return points


def min_manhattan(first, second):
    return min(abs(x) + abs(y) for (x, y) in get_points(first) & get_points(second) if (x, y) != (0, 0))


assert 6 == min_manhattan('R8,U5,L5,D3', 'U7,R6,D4,L4')
assert 159 == min_manhattan('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83')
assert 135 == min_manhattan('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7')


with open('input') as f:
    input = f.read().splitlines()
print(min_manhattan(input[0], input[1]))
