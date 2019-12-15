from ..intcode import IntCode
import collections
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
Opcode 9 adjusts the relative base by the value of its only parameter. The relative base increases (or decreases, if the value is negative) by the value of the parameter
'''
import sys

BUF = list(0 for i in range(1000))

class RelativeBase:
    def __init__(self, v):
        self.v = 0

class Register:
    def __init__(self, input=[1], inc=False, output=0):
        self.input = input
        self.output = 0
        self._index = 0
        self.inc = inc

    def input_instruction(self):
        if not self.inc:
            return self.input[0]

        # temporarily out of input instructions
        if not self._index < len(self.input):
            return None

        rv = self.input[self._index]
        self._index = self._index + 1
        return rv

    def set_input(self, input):
        self.input = input
        self._index = 0

class BlockedException(Exception):
    def __init__(self, ip, program):
        self.ip = ip
        self.program = program

# TODO refactor this to not use global mutation
master_register = Register(input=[1], output=0)
relative_base = RelativeBase(0)

def _register(program, modes, ip, idx):
    if modes[idx] == 1:
        return program[ip + idx]
    if modes[idx] == 2:
        return program[relative_base.v + program[ip + idx]]
    else:
        return program[program[ip + idx]]

def add(ip, program, modes):
    p = program.copy()
    r1 = _register(p, modes, ip, 1)
    r2 = _register(p, modes, ip, 2)
    r3 = p[ip + 3]
    if modes[3] == 2:
        r3 = p[relative_base.v + p[ip + 3]]

    p[r3] = r1 + r2
    return (ip + 4, p)

def mult(ip, program, modes):
    p = program.copy()
    r1 = _register(p, modes, ip, 1)
    r2 = _register(p, modes, ip, 2)
    r3 = p[ip + 3]
    if modes[3] == 2:
        r3 = p[relative_base.v + p[ip + 3]]

    p[r3] = r1 * r2
    return (ip + 4, p)

def save(ip, program, modes):
    p = program.copy()
    instr = master_register.input_instruction()
    if instr == None:
        raise BlockedException(ip, p)

    if modes[1] == 2:
        p[relative_base.v + p[ip + 1]] = instr
    else:
        p[p[ip + 1]] = instr

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
    if modes[3] == 2:
        r3 = p[relative_base.v + p[ip + 3]]
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
    if modes[3] == 2:
        r3 = p[relative_base.v + p[ip + 3]]
    if r1 == r2:
        p[r3] = 1
    else:
        p[r3] = 0
    return (ip + 4, p)

def rb(ip, program, modes):
    p = program.copy()
    r1 = _register(p, modes, ip, 1)
    relative_base.v = relative_base.v + r1
    return (ip + 2, p)

opcodes = {
    1 : lambda ip, program, modes: add(ip, program, modes),
    2 : lambda ip, program, modes: mult(ip, program, modes),
    3 : lambda ip, program, modes: save(ip, program, modes),
    4 : lambda ip, program, modes: iden(ip, program, modes),
    5 : lambda ip, program, modes: jit(ip, program, modes),
    6 : lambda ip, program, modes: jif(ip, program, modes),
    7 : lambda ip, program, modes: lt(ip, program, modes),
    8 : lambda ip, program, modes: eq(ip, program, modes),
    9 : lambda ip, program, modes: rb(ip, program, modes),
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

assert relative_base.v == 0
assert (2, [9, 1, 1, 1]) == opcodes[9](0, [9, 1, 1, 1], split_modes(100))
assert relative_base.v == 1

relative_base.v = 2
assert (4, [1, 1, 0, 4, 4]) == opcodes[1](0, [1, 1, 0, 4, 0], split_modes(1200))


def execute(program, input=[1], ip=0):
    master_register.output = 0
    relative_base.v = 0
    master_register.set_input(input)
    while True:
        try:
            modes = split_modes(program[ip])
            print(ip)
            (ip, program) = opcodes[modes[0]](ip, program, modes)
        except KeyError:
            return program

assert [2, 0, 0, 0, 99] == execute([1, 0, 0, 0, 99])
assert [2, 3, 0, 6, 99] == execute([2, 3, 0, 3, 99])
assert [2, 4, 4, 5, 99, 9801] == execute([2, 4, 4, 5, 99, 0])
assert [30, 1, 1, 4, 2, 5, 6, 0, 99] == execute([1, 1, 1, 4, 99, 5, 6, 0, 99])


execute([104,1125899906842624,99] + BUF)
assert 1125899906842624 == master_register.output

print('>>>> BEGIN Quine')
execute([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99] + BUF)
print('<<<< END Quine')

execute([1102,34915192,34915192,7,4,7,99,0])

with open('input') as f:
    input = [int(s) for s in f.read().split(',')]
    print('>>>> BEGIN PROGRAM')
    execute(input + BUF, input=[1], ip=0)
    print('<<<< END PROGRAM')
    print(master_register.output)
