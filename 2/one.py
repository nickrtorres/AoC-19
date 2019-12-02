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
    input = [int(x) for x in f.read().split(',')]


assert 2 < len(input)
input[1] = 12
input[2] = 2


print(process(input)[0])
