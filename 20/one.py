import heapq
import string
import collections
import re

import data

PATH = '.'
WALL = '#'

SIMPLE_PUZZLE = '''\
         A
         A
  #######.#########
  #######.........#
  #######.#######.#
  #######.#######.#
  #######.#######.#
  #####  B    ###.#
BC...##  C    ###.#
  ##.##       ###.#
  ##...DE  F  ###.#
  #####    G  ###.#
  #########.#####.#
DE..#######...###.#
  #.#########.###.#
FG..#########.....#
  ###########.#####
             Z
             Z
'''

COMPLEX_PUZZLE = '''\
                   A
                   A
  #################.#############
  #.#...#...................#.#.#
  #.#.#.###.###.###.#########.#.#
  #.#.#.......#...#.....#.#.#...#
  #.#########.###.#####.#.#.###.#
  #.............#.#.....#.......#
  ###.###########.###.#####.#.#.#
  #.....#        A   C    #.#.#.#
  #######        S   P    #####.#
  #.#...#                 #......VT
  #.#.#.#                 #.#####
  #...#.#               YN....#.#
  #.###.#                 #####.#
DI....#.#                 #.....#
  #####.#                 #.###.#
ZZ......#               QG....#..AS
  ###.###                 #######
JO..#.#.#                 #.....#
  #.#.#.#                 ###.#.#
  #...#..DI             BU....#..LF
  #####.#                 #.#####
YN......#               VT..#....QG
  #.###.#                 #.###.#
  #.#...#                 #.....#
  ###.###    J L     J    #.#.###
  #.....#    O F     P    #.#...#
  #.###.#####.#.#####.#####.###.#
  #...#.#.#...#.....#.....#.#...#
  #.#####.###.###.#.#.#########.#
  #...#.#.....#...#.#.#.#.....#.#
  #.###.#####.###.###.#.#.#######
  #.#.........#...#.............#
  #########.###.###.#############
           B   J   C
           U   P   P
'''

def _unreachable():
    raise RuntimeError("Something really bad happened. aborting now...")

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

def _neighbor_direction(og, neighbor):
    if neighbor[0] < og[0]:
        return LEFT
    elif neighbor[0] > og[0]:
        return RIGHT
    elif neighbor[1] < og[1]:
        return UP
    elif neighbor[1] > og[1]:
        return DOWN
    else:
        _unreachable()

assert LEFT == _neighbor_direction((1,0), (0,0))
assert RIGHT == _neighbor_direction((0,0), (1,0))
assert UP == _neighbor_direction((0,1), (0,0))
assert DOWN == _neighbor_direction((0,0), (0,1))

def get_neighbors(puzzle_lines, row, col):
    upper_row = len(puzzle_lines)
    upper_col = max((len(line) for line in puzzle_lines))

    neighbors = ((r, c) for r,c in [(row + 1, col), (row - 1, col), (row, col - 1), (row, col + 1)] if r >= 0  and r < upper_row and c >= 0 and c < upper_col)

    # only include the neighbors that actually exist in the map.
    # that is, a coordinate is invalid if we step off the end of
    # a row while validating a coordinate
    valid_coordinates = []
    for r, c in neighbors:
        try:
            puzzle_lines[r][c]
            valid_coordinates.append((r,c))
        except IndexError:
            pass
    return valid_coordinates

def node_name(puzzle_lines, known):
    '''
    nodes are always read and stored top to bottom, left to right:

        A
        B      ---> 'AB'
       #.#

       #.#
        A      ---> 'AB'
        B

        #
      AB.      ---> 'AB'
        #

        #
        .AB    ---> 'AB'
        #
    '''
    row, col = known
    neighbors = get_neighbors(puzzle_lines, row, col)
    prime = puzzle_lines[row][col]

    for neighbor in neighbors:
        neighbor_alpha = puzzle_lines[neighbor[0]][neighbor[1]]
        if neighbor_alpha in string.ascii_uppercase:
            direction = _neighbor_direction(known, neighbor)

            if direction == UP or direction == LEFT:
                return neighbor_alpha + puzzle_lines[row][col]
            else:
                return puzzle_lines[row][col] + neighbor_alpha

    _unreachable()

assert 'BC' == node_name(SIMPLE_PUZZLE.splitlines() ,(7, 9))
assert 'BC' == node_name(SIMPLE_PUZZLE.splitlines() ,(8, 1))
assert 'AS' == node_name(COMPLEX_PUZZLE.splitlines() ,(17, 33))

def find_leafs(puzzle):
    puzzle_lines = puzzle.splitlines()
    upper_row = len(puzzle_lines)
    upper_col = max((len(line) for line in puzzle_lines))

    starts = []
    alphas = set(string.ascii_uppercase)
    for row, line in enumerate(puzzle_lines):
        for col in range(len(line)):
            if line[col] in alphas:
                starts.append((row, col))

    # A given starting point will be adjacent to one and only one '.'
    leafs = []
    for row, col in starts:
        cardinals = get_neighbors(puzzle_lines, row, col)
        for dir in cardinals:
            if puzzle_lines[dir[0]][dir[1]] == '.':
                leafs.append((dir, node_name(puzzle_lines, (row, col)), (row, col)))
    return leafs

def inverse_node(node, others):
    return next((n for n in others if n.name == node.name and n != node), data.Node())

assert data.Node() != inverse_node(data.Node(name='AB', entry=(1,1)), [data.Node(name='AB', entry=(0,0)), data.Node(name='AB', entry=(1,1))])
assert data.Node(name='AB', entry=(0,0)) == inverse_node(data.Node(name='AB', entry=(1,1)), [data.Node(name='AB', entry=(0,0)), data.Node(name='AB', entry=(1,1))])

def build(puzzle):
    puzzle_lines = puzzle.splitlines()

    nodes = []
    leafs = collections.deque()
    leaf_entry = {}
    for leaf, name, cord  in find_leafs(puzzle):
        leaf_entry[leaf] = (name, cord)
        leafs.append((leaf, 0))

    while len(leafs) > 0:
        top, _ = leafs[0]
        visited = set()
        q = collections.deque()
        q.append(leafs.popleft())
        while len(q) > 0:
            current, cost = q.popleft()
            if current not in visited:
                visited.add(current)
            else:
                continue

            for row, col in get_neighbors(puzzle_lines, *current):
                if puzzle_lines[row][col] == PATH:
                    if (row, col) not in visited:
                        q.append(((row, col), cost + 1))
                elif puzzle_lines[row][col] != WALL and (row, col) != leaf_entry[top][1]:
                    found = data.Node(name=node_name(puzzle_lines, (row,col)), entry=(row,col))
                    try:
                        _ = nodes.index(found)
                    except ValueError:
                        nodes.append(found)

                    n = data.Node(name=leaf_entry[top][0], entry=leaf_entry[top][1], neighbors=set([data.Path(end=found, path_cost=cost)]))
                    try:
                        idx = nodes.index(n)
                        nodes[idx] = n + nodes[idx]
                    except ValueError:
                        nodes.append(n)

    return nodes

def search(l, f):
    for i in range(len(l)):
        if f(l[i]):
            return i
    raise ValueError

assert search([1,2,3,4,5], lambda x: x == 2) == 1

def process(current=data.Route(), path=data.Path(), heap=[], overhead=0, o=dict()):
    try:
        idx = search(heap, lambda route: route.node== path.end)
        if heap[idx].net_cost > (path.path_cost + overhead + current.net_cost):
            heap[idx].net_cost = (path.path_cost + overhead + current.net_cost)
            heap[idx].via = current
            heapq.heapify(heap)

    except ValueError:
            heap.append(data.Route(node=o[(path.end.name, path.end.entry)], net_cost=(path.path_cost + overhead + current.net_cost), via=current))
            heapq.heapify(heap)

def _dijkstra_debug(visited, end='ZZ'):
    bt = visited[end]
    while bt != None:
        print(f'node => {bt.node.name}; net_cost => {bt.net_cost}')
        bt = bt.via

def dijkstra(nodes, start='AA', end='ZZ'):
    s = next((n for n in nodes if n.name == start), None)
    e = next((n for n in nodes if n.name == end), None)
    others = dict(((n.name, n.entry), n) for n in nodes)

    heap = []
    heapq.heappush(heap, data.Route(node=s, net_cost=0, via=None))

    visited = { start: s }
    while len(heap) != 0:
        current = heapq.heappop(heap)
        visited[current.node.name] = current

        for path in current.node.neighbors:
            if path.end.name not in visited:
                process(current=current, path=path, heap=heap, overhead=0, o=others)

        for path in inverse_node(current.node, nodes).neighbors:
            if path.end.name not in visited:
                process(current=current, path=path, heap=heap, overhead=1, o=others)

    if __debug__:
        _dijkstra_debug(visited)

    return visited[end].net_cost

assert dijkstra(build(SIMPLE_PUZZLE)) == 23
assert dijkstra(build(COMPLEX_PUZZLE)) == 58

with open('input') as f:
    puzzle = f.read()
    print(dijkstra(build(puzzle)))
