import itertools
import operator

def as_list(x):
    return [int(s) for s in str(x)]

def string_as_list(x):
    return [int(s) for s in x]


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


transparent = 2
white = 1
black = 0

def count_num(tuples, num):
    return sum(x == num for x in itertools.chain(*tuples))

def collapse_to_visible(column):
    for color in column:
        if color != transparent:
            return color
    return transparent

def print_vec_as_mat(vec, dim=(0,0)):
    x, _ = dim
    
    count = 0
    for p in vec:
        count = count + 1
        if count == x:
            e = '\n'
            count = 0
        else:
            e = ''

        print(p, end=e)
    print()


    

assert 0 == collapse_to_visible([2, 0, 1])
assert 1 == collapse_to_visible([2, 2, 1])
assert 2 == collapse_to_visible([2, 2, 2])
    

assert 4 == count_num([(0, 1), (1, 0), (1, 1)], 1)
assert 0 == count_num([(1, 1), (1, 1), (1, 1)], 0)

def collapse_at_index(iterable, idx):
    out = []
    for layer in iterable:
        row = list(itertools.chain(*layer))
        out.append(row[idx])
    return out

assert [1, 2, 3] == collapse_at_index([[(1, 2), (3, 4)], [(2, 3)], [(3, 4)]], 0)
ex = [[(0, 2), (2, 2)], [(1, 1), (2, 2)], [(2, 2), (1, 2)], [(0, 0), (0, 0)]]
points = [collapse_at_index(ex, 0)]
points.append(collapse_at_index(ex, 1))
points.append(collapse_at_index(ex, 2))
points.append(collapse_at_index(ex, 3))
print_vec_as_mat([collapse_to_visible(x) for x in points], dim=(2,2))


DIM = (25, 6)

with open('input') as f:
    d = string_as_list(f.read().strip())

    processed = decode(d, dim=DIM)
    points = [collapse_at_index(processed, i) for i in range(DIM[0])]
    print(len(points))
    for point in points:
        print(point)
    print([collapse_to_visible(x) for x in points])


