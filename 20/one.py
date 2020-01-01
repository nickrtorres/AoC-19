import heapq
import string
import collections
import re

PATH = '.'
WALL = '#'
BLANK = ' '
EMPTY = ''

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

    return [(r, c) for r,c in [(row + 1, col), (row - 1, col), (row, col - 1), (row, col + 1)] if r >= 0  and r < upper_row and c >= 0 and c < upper_col]

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
        cardinals = [(r, c) for r,c in [(row + 1, col), (row - 1, col), (row, col - 1), (row, col + 1)] if r >= 0  and r < upper_row and c >= 0 and c < upper_col]
        for dir in cardinals:
            try:
                if puzzle_lines[dir[0]][dir[1]] == '.':
                    leafs.append((dir, node_name(puzzle_lines, (row, col)), (row, col)))
            except IndexError:
                # stepped off the end of an incomplete row.
                # we don't really care about this state (i think)
                pass
    return leafs

class Path:
    def __init__(self, end=None, path_cost=0):
        self.end = end
        self.path_cost = path_cost

    def __eq__(self, other):
        if not isinstance(other, Path):
            return false

        return self.end == other.end and self.path_cost == other.path_cost

    def __hash__(self):
        return hash(self.end) + hash(self.path_cost)

    def __lt__(self, other):
        if not isinstance(other, Path):
            return False
        return self.path_cost < other.path_cost


class Node:
    def __init__(self, entry=(0,0), name='', neighbors=set()):
        self.entry = entry
        self.name = name
        self.neighbors = neighbors

    def __add__(self, other):
        if not isinstance(other, Node):
            raise RuntimeError("invalid operand")

        return Node(name=self.name, entry=self.entry, neighbors=self.neighbors.union(other.neighbors))

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False

        return self.name == other.name and self.entry == other.entry

    def __hash__(self):
        return hash(self.entry) + hash(self.name)

def inverse_node(node, others):
    return next((n for n in others if n.name == node.name and n != node), None)

assert None != inverse_node(Node(name='AB', entry=(1,1)), [Node(name='AB', entry=(0,0)), Node(name='AB', entry=(1,1))])
assert Node(name='AB', entry=(0,0)) == inverse_node(Node(name='AB', entry=(1,1)), [Node(name='AB', entry=(0,0)), Node(name='AB', entry=(1,1))])

def build(puzzle):
    puzzle_lines = puzzle.splitlines()

    nodes = []
    leafs = collections.deque()
    leaf_entry = {}
    for leaf, name, cord  in find_leafs(puzzle):
        leaf_entry[leaf] = (name, cord)
        leafs.append((leaf, 0))

    costs = collections.defaultdict(list)
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

            for row, col in get_neighbors(puzzle_lines, current[0], current[1]):
                costs[(row,col)].append(cost)
                try:
                    if puzzle_lines[row][col] == PATH:
                        if (row, col) not in visited:
                            q.append(((row, col), cost + 1))
                    elif puzzle_lines[row][col] != WALL and (row, col) != leaf_entry[top][1]:
                        found = Node(name=node_name(puzzle_lines, (row,col)), entry=(row,col))
                        try:
                            _ = nodes.index(found)
                        except ValueError:
                            nodes.append(found)

                        n = Node(name=leaf_entry[top][0], entry=leaf_entry[top][1], neighbors=set([Path(end=found, path_cost=cost)]))
                        try:
                            idx = nodes.index(n)
                            nodes[idx] = n + nodes[idx]
                        except ValueError:
                            nodes.append(n)
                except IndexError:
                    # (again) stepped off the end of an incomplete row.
                    # we don't really care about this state (i think)
                    pass

    return nodes

class Route:
    def __init__(self, node=None, net_cost=0, via=None):
        self.node = node
        self.net_cost = net_cost
        self.via = via

    def __eq__(self, other):
        if not isinstance(other, Route):
            return False
        return self.node == other.node

    def __lt__(self, other):
        if not isinstance(other, Route):
            return False

        return self.net_cost < other.net_cost

def search(l, f):
    for i in range(len(l)):
        if f(l[i]):
            return i
    raise ValueError
assert search([1,2,3,4,5], lambda x: x == 2) == 1

def dijkstra(nodes, start='AA', end='ZZ'):
    s = next((n for n in nodes if n.name == start), None)
    e = next((n for n in nodes if n.name == end), None)
    others = dict(((n.name, n.entry), n) for n in nodes)

    heap = []
    heapq.heappush(heap, Route(node=s, net_cost=0, via=None))

    visited = { start: s }
    while len(heap) != 0:
        current = heapq.heappop(heap)
        visited[current.node.name] = current

        for path in current.node.neighbors:
            if path.end.name in visited:
                continue

            try:
                idx = search(heap, lambda route: route.node.name == path.end.name)
                if heap[idx].net_cost > (path.path_cost + current.net_cost):
                    heap[idx].net_cost = (path.path_cost + current.net_cost)
                    heap[idx].via = current
                    heapq.heapify(heap)

            except ValueError:
                heap.append(Route(node=others[(path.end.name, path.end.entry)], net_cost=(path.path_cost + current.net_cost), via=current))
                heapq.heapify(heap)

        try:
            for path in inverse_node(current.node, nodes).neighbors:
                # teleporting incurs an overhead 1
                overhead = 1
                if path.end.name in visited:
                    continue

                try:
                    idx = search(heap, lambda route: route.node == path.end)
                    if heap[idx].net_cost > (path.path_cost + overhead + current.net_cost):
                        heap[idx].net_cost = (path.path_cost + overhead + current.net_cost)
                        heap[idx].via = current
                        heapq.heapify(heap)

                except ValueError:
                    heap.append(Route(node=others[(path.end.name, path.end.entry)], net_cost=(path.path_cost + overhead + current.net_cost), via=current))
                    heapq.heapify(heap)
        except AttributeError:
            pass

    return visited[end].net_cost


#for node in build(SIMPLE_PUZZLE):
#    print(node.name)
#    for p in sorted(node.neighbors):
#        print(f'\t {p.end.name} => {p.path_cost}')

assert dijkstra(build(SIMPLE_PUZZLE)) == 23
assert dijkstra(build(COMPLEX_PUZZLE)) == 58

with open('input') as f:
    puzzle = f.read()
    print(dijkstra(build(puzzle)))
