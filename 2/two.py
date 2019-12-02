import itertools

opcodes = {
    1 : lambda left, right: left + right,
    2 : lambda left, right: left * right
}


def process(program):
    step, ip = 4, 0

    while True:
        try:
            opcode = opcodes[program[ip]]
            left = program[program[ip + 1]]
            right = program[program[ip + 2]]
            program[program[ip + 3]] = opcode(left, right)
            ip += step
        except KeyError:
            return program


assert [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50] == process([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
assert [2, 0, 0, 0, 99] == process([1, 0, 0, 0, 99])
assert [2, 3, 0, 6, 99] == process([2, 3, 0, 3, 99])
assert [2, 4, 4, 5, 99, 9801] == process([2, 4, 4, 5, 99, 0])
assert [30, 1, 1, 4, 2, 5, 6, 0, 99] == process([1, 1, 1, 4, 99, 5, 6, 0, 99])


with open('input') as f:
    clean_input = [int(x) for x in f.read().split(',')]


assert 2 < len(clean_input)


TARGET = 19690720
for (noun, verb) in itertools.permutations(range(100), 2):
    input = clean_input.copy()
    input[1], input[2] = noun, verb

    if process(input)[0] == TARGET:
        print(100 * noun + verb)
