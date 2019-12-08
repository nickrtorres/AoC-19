import itertools
'''
Opcode 1 adds together numbers read from two positions and stores the result in a third position.
Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
Opcode 3 takes a single integer as input and saves it to the position given by its only parameter
Opcode 4 outputs the value of its only parameter
Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
'''

class Register:
    def __init__(self, input=1, output=0):
        self.input = 1
        self.output = 0

# TODO refactor this to not use global mutation
master_register = Register(input=8, output=0)

def _register(program, modes, ip, idx):
    if modes[idx] == 1:
        return program[ip + idx]
    else:
        return program[program[ip + idx]]

def add(ip, program, modes):
    p = program.copy()
    r1 = _register(p, modes, ip, 1)
    r2 = _register(p, modes, ip, 2)
    r3 = p[ip + 3]
    p[r3] = r1 + r2
    return (ip + 4, p)

def mult(ip, program, modes):
    p = program.copy()
    r1 = _register(p, modes, ip, 1)
    r2 = _register(p, modes, ip, 2)
    r3 = p[ip + 3]
    p[r3] = r1 * r2
    return (ip + 4, p)

def save(ip, program, modes):
    p = program.copy()
    p[p[ip + 1]] = master_register.input
    return (ip + 2, p)

def iden(ip, program, modes):
    p = program.copy()
    r1 = _register(p, modes, ip, 1)
    master_register.output = r1
    return (ip + 2, p)

def jit(ip, program, modes):
    p = program.copy()
    r1 = _register(p, modes, ip, 1)
    r2 = _register(p, modes, ip, 2)
    if r1 != 0:
        return (r2, p)
    else:
        return (ip + 3, p)

def  jif(ip, program, modes):
    p = program.copy()
    r1 = _register(p, modes, ip, 1)
    r2 = _register(p, modes, ip, 2)
    if r1 == 0:
        return (r2, p)
    else:
        return (ip + 3, p)

def  lt(ip, program, modes):
    p = program.copy()
    r1 = _register(p, modes, ip, 1)
    r2 = _register(p, modes, ip, 2)
    r3 = p[ip + 3]
    if r1 < r2:
        p[r3] = 1
    else:
        p[r3] = 0
    return (ip + 4, p)

def  eq(ip, program, modes):
    p = program.copy()
    r1 = _register(p, modes, ip, 1)
    r2 = _register(p, modes, ip, 2)
    r3 = p[ip + 3]
    if r1 == r2:
        p[r3] = 1
    else:
        p[r3] = 0
    return (ip + 4, p)

opcodes = {
    1 : lambda ip, program, modes: add(ip, program, modes),
    2 : lambda ip, program, modes: mult(ip, program, modes),
    3 : lambda ip, program, modes: save(ip, program, modes),
    4 : lambda ip, program, modes: iden(ip, program, modes),
    5 : lambda ip, program, modes: jit(ip, program, modes),
    6 : lambda ip, program, modes: jif(ip, program, modes),
    7 : lambda ip, program, modes: lt(ip, program, modes),
    8 : lambda ip, program, modes: eq(ip, program, modes),
}

def split_modes(input):
    modes = [input % 100]
    input //= 100
    for i in range(1, 4 + 1):
        modes.append(input % 10)
        input //= 10
    return modes

assert [2, 0, 1, 0, 0] == split_modes(1002)

assert (4, [1002, 4, 3, 4, 36]) == opcodes[1](0, [1002, 4, 3, 4, 33], split_modes(1002))
assert (4, [2, 0, 0, 0]) == opcodes[1](0, [1, 0, 0, 0], split_modes(0))
assert (4, [1002, 4, 3, 4, 99]) == opcodes[2](0, [1002, 4, 3, 4, 33], split_modes(1002))
assert (4, [2, 3, 0, 6]) == opcodes[2](0, [2, 3, 0, 3], split_modes(0))
assert (2, [3, 2, 1]) == opcodes[3](0, [3, 2, 0], split_modes(0))
assert (2, [4, 2, 0]) == opcodes[4](0, [4, 2, 0], split_modes(0))
assert (2, [4, 2, 0]) == opcodes[4](0, [4, 2, 0], split_modes(111))
assert (2, [5, 0, 2]) == opcodes[5](0, [5, 0, 2], split_modes(0))
assert (3, [5, 0, 2]) == opcodes[5](0, [5, 0, 2], split_modes(100))
assert (3, [6, 0, 2]) == opcodes[6](0, [6, 0, 2], split_modes(0))
assert (2, [6, 0, 2]) == opcodes[6](0, [6, 0, 2], split_modes(100))
assert (4, [7, 0, 1, 1]) == opcodes[7](0, [7, 0, 1, 1], split_modes(0))
assert (4, [7, 1, 1, 1]) == opcodes[7](0, [7, 0, 1, 1], split_modes(1100))
assert (4, [1, 0, 0, 0]) == opcodes[8](0, [8, 0, 0, 0], split_modes(0))
assert (4, [8, 0, 1, 1]) == opcodes[8](0, [8, 0, 1, 1], split_modes(1100))


def execute(program, input=1):
    master_register.input = input
    program = program.copy()
    ip = 0
    while True:
        try:
            modes = split_modes(program[ip])
            (ip, program) = opcodes[modes[0]](ip, program, modes)
        except KeyError:
            return program

assert [2, 0, 0, 0, 99] == execute([1, 0, 0, 0, 99])
assert [2, 3, 0, 6, 99] == execute([2, 3, 0, 3, 99])
assert [2, 4, 4, 5, 99, 9801] == execute([2, 4, 4, 5, 99, 0])
assert [30, 1, 1, 4, 2, 5, 6, 0, 99] == execute([1, 1, 1, 4, 99, 5, 6, 0, 99])


execute([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8)
assert 1 == master_register.output

execute([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 1)
assert 0 == master_register.output

execute([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 1)
assert 1 == master_register.output

execute([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 100)
assert 0 == master_register.output

execute([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8)
assert 1 == master_register.output

execute([3, 3, 1108, -1, 8, 3, 4, 3, 99], 1)
assert 0 == master_register.output

execute([3, 3, 1107, -1, 8, 3, 4, 3, 99], 1)
assert 1 == master_register.output

execute([3, 3, 1107, -1, 8, 3, 4, 3, 99], 9)
assert 0 == master_register.output

execute([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0)
assert 0 == master_register.output

execute([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1)
assert 1 == master_register.output

execute([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0)
assert 0 == master_register.output

execute([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1)
assert 1 == master_register.output

execute([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], 4)


with open('input') as f:
    clean_input = [int(s) for s in f.read().strip().split(',')]
    program = clean_input.copy()
    execute(program, 1)
    print(f'part 1 => { master_register.output }')
    execute(program, 5)
    print(f'part 2 => { master_register.output }')
