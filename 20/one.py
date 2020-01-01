import string
import collections
import re

PATH = '.'
WALL = '#'
BLANK = ' '
EMPTY = ''

SIMPLE_PUZZLE = r'''
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
'''.lstrip('\n')

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

    '''
    A given starting point will be adjacent to one and only one '.'
    '''
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

        if self.name != other.name:
            return False

        return self.entry == other.entry
        
    def __hash__(self):
        return hash(self.entry) + hash(self.name)

def inverse_node(node, others):
    return next((n for n in others if n.name == node.name and n != node), None)

assert None != inverse_node(Node(name='AB', entry=(1,1)), [Node(name='AB', entry=(0,0)), Node(name='AB', entry=(1,1))])
assert Node(name='AB', entry=(0,0)) == inverse_node(Node(name='AB', entry=(1,1)), [Node(name='AB', entry=(0,0)), Node(name='AB', entry=(1,1))])

def build(puzzle):
    print(puzzle)
    puzzle_lines = puzzle.splitlines()

    nodes = []
    leafs = collections.deque()
    leaf_entry = {}
    for leaf, name, cord  in find_leafs(puzzle):
        leaf_entry[leaf] = (name, cord)
        leafs.append(leaf)



    while len(leafs) > 0:
        cost = 0
        top = leafs[0]
        visited = set()
        q = collections.deque()
        q.append(leafs.popleft())
        while len(q) > 0:
            current = q.popleft()
            if current not in visited:
                visited.add(current)
            else:
                continue

            for row, col in get_neighbors(puzzle_lines, current[0], current[1]):
                try:
                    if puzzle_lines[row][col] == PATH:
                        if (row, col) not in visited:
                            q.append((row, col))
                    elif puzzle_lines[row][col] != WALL and (row, col) != leaf_entry[top][1]:
                        found = Node(name=node_name(puzzle_lines, (row,col)), entry=(row,col))
                        try:
                            _ = nodes.index(found)
                        except ValueError:
                            nodes.append(found)

                        n = Node(name=leaf_entry[top][0], entry=leaf_entry[top][1], neighbors=set())
                        try:
                            idx = nodes.index(n)
                            nodes[idx] = n + nodes[idx]
                        except ValueError:
                            nodes.append(n)
                except IndexError:
                    # (again) stepped off the end of an incomplete row.
                    # we don't really care about this state (i think)
                    pass
            # FIXME: cost calculation is bork'd
            cost += 1

    for n in nodes:
        print(n.name, n.entry)

build(SIMPLE_PUZZLE)
