import itertools
import operator

def as_list(x):
    return [int(s) for s in str(x)]


def decode(input, dim=(0, 0)):
    x, y = dim
    idx = 0
    ycount = 0
    outer = []
    while idx < len(input):
        inner = []
        while idx < len(input) and ycount < y:
            inner.append(tuple(input[idx:idx+x]))
            idx = idx + x
            ycount = ycount + 1
        outer.append(inner)
        ycount = 0
    return outer

        

assert [[(1, 2)]] == decode(as_list(12), dim=(2, 1))
assert [[(1, 2, 3), (4, 5, 6)]] == decode(as_list(123456), dim=(3, 2))
assert [[(1, 2, 3), (4, 5, 6)], [(7, 8, 9), (0, 1, 2)]] == decode(as_list(123456789012), dim=(3, 2))
assert [[(1, 2, 3, 4, 5), (6, 7, 8, 9, 0)], [(1, 2, 3, 4, 5), (6, 7, 8, 9, 0)]] == decode(as_list(12345678901234567890), dim=(5, 2))

assert [[(2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1), (2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1)], [(2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1), (2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1)], [(2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1), (2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1)]] ==  decode(as_list(221111111101112211211111122111111110111221121111112211111111011122112111111221111111101112211211111122111111110111221121111112211111111011122112111111), dim=(25, 2))

def count_num(tuples, num):
    return sum(x == num for x in itertools.chain(*tuples))

assert 4 == count_num([(0, 1), (1, 0), (1, 1)], 1)
assert 0 == count_num([(1, 1), (1, 1), (1, 1)], 0)

def calculate(input, dim):
    layers = []
    for layer in decode(as_list(input), dim=dim):
        layers.append((layer, count_num(layer, 0)))
    
    least_zeros = min(layers, key=operator.itemgetter(1))[0]
    return count_num(least_zeros, 1) * count_num(least_zeros, 2) 

assert 1 == calculate(123456789012, dim=(3, 2))
assert 1 == calculate(12345678901234567890, dim=(5, 2))
assert 4 == calculate(12245678101234567800, dim=(5, 2))
assert 6 == calculate(11222555550000000000, dim=(5, 2))
assert 95 == calculate(2211111111011122112111111, dim=(25,1))

DIM = (25, 6)
with open('input') as f:
    input = int(f.read())
print(calculate(input, dim=DIM))
