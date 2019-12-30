import itertools

BASE = [0, 1, 0, -1]

def _fft_core(input_list, program_len=0):
    program = [int(c) for c in input_list]

    output = []
    for i in range(1, program_len + 1):
        pattern = itertools.cycle(itertools.chain.from_iterable(itertools.repeat(x, i) for x in BASE))
        pattern.__next__() # shift left by one
        output.append(sum((l*p for l, p in zip(program, pattern))))

    return [abs(o) % 10 for o in output]

assert _fft_core('12345678', program_len=8) == [4, 8, 2, 2, 6, 1, 5, 8]
assert _fft_core('12345678', program_len=8) == [4, 8, 2, 2, 6, 1, 5, 8]
assert _fft_core('48226158', program_len=8) == [3, 4, 0, 4, 0, 4, 3, 8]
assert _fft_core('34040438', program_len=8) == [0, 3, 4, 1, 5, 5, 1, 8]
assert _fft_core('03415518', program_len=8) == [0, 1, 0, 2, 9, 4, 9, 8]

def fft(input_list, phases=1):
    pl = len(str(input_list))
    for i in range(phases):
        input_list = _fft_core(input_list, program_len=pl)

    return ''.join((str(i) for i in input_list))

assert fft('12345678', phases=4) == '01029498'
assert fft('80871224585914546619083218645595', phases=100)[:8] == '24176176'
assert fft('19617804207202209144916044189917', phases=100)[:8] == '73745418'
assert fft('69317163492948606335995924319873', phases=100)[:8] == '52432133'

with open('input') as f:
    puzzle = f.read()
    assert fft(puzzle, phases=100)[:8] == '32002835'
