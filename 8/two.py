import itertools

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


def count_num(tuples, num):
    return sum(x == num for x in itertools.chain(*tuples))

assert 4 == count_num([(0, 1), (1, 0), (1, 1)], 1)
assert 0 == count_num([(1, 1), (1, 1), (1, 1)], 0)


def print_vec_as_mat(vec, dim=(0,0)):
    x, _ = dim
    
    count = 0
    for p in vec:
        out = ' ' if p == 0 else '#'
        count = count + 1
        if count == x:
            e = '\n'
            count = 0
        else:
            e = ''

        print(out, end=e)
    print()


with open('input') as f:
    DIM = (25, 6)
    d = string_as_list(f.read().strip())

    processed = decode(d, dim=DIM)
    image = []
    for i in range(25 * 6):
        for layer in processed:
            flattened = list(itertools.chain(*layer))
            if flattened[i] != 2:
                image.append(flattened[i])
                break
    print_vec_as_mat(image, (25,6))
