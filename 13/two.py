import sys, os
import collections
sys.path.insert(0, os.path.abspath('../intcode'))
import intcode

# globals :(
g_stockpile = []
g_output = []


Tile = collections.namedtuple('Tile', 'x y id')

def store(register):
    global g_stockpile
    global g_output

    g_stockpile.append(register)
    if len(g_stockpile) == 3:
        g_output.append(Tile(x=g_stockpile[0], y=g_stockpile[1], id=g_stockpile[2]))
        g_stockpile = []

with open('input') as f:
    input = [int(s) for s in f.read().split(',')]

    input[0] = 2
    computer = intcode.IntCode(input, observer=store)
    computer.execute()

    print([tile for tile in g_output if tile.x == -1  and tile.y == 0])
