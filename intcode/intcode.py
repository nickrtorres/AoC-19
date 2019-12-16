def _split_modes(input):
    modes = [input % 100]
    input //= 100
    for i in range(1, 4 + 1):
        modes.append(input % 10)
        input //= 10
    return modes


class IntCode:
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
    _opcodes = {
        1 : lambda self, modes: self._add(modes),
        2 : lambda self, modes: self._mult(modes),
        3 : lambda self, modes: self._save(modes),
        4 : lambda self, modes: self._iden(modes),
        5 : lambda self, modes: self._jit(modes),
        6 : lambda self, modes: self._jif(modes),
        7 : lambda self, modes: self._lt(modes),
        8 : lambda self, modes: self._eq(modes),
        9 : lambda self, modes: self._rb(modes),
    }


    def execute(self):
        while True:
            try:
                modes = _split_modes(self.program[self.ip])
                self._opcodes[modes[0]](self, modes)
            except IndexError:
                self.program = self.program + [0 for _ in range(len(self.program))]
            except KeyError:
                break

    def output(self, register):
        self.output_register = register

        if self.observer is not None:
            self.output_queue.append(register)
            if len(self.output_queue) == self.output_step:
                self.observer(tuple(self.output_queue))
                self.output_queue = []


    def _get_input(self):
        if self.driver:
            return self.driver()
        return self.input_register


    def __init__(self, program, observer=None, driver=None, output_step=1):
        self.program = program
        self.input_register = 0
        self.output_register = 0
        self.ip = 0
        self.relative_base = 0
        self.observer = observer
        self.driver = driver
        self.output_queue = []
        self.output_step = output_step


    def _register(self, modes, idx):
        if modes[idx] == 1:
            return self.program[self.ip + idx]
        if modes[idx] == 2:
            return self.program[self.relative_base + self.program[self.ip + idx]]
        else:
            return self.program[self.program[self.ip + idx]]
    

    def _add(self, modes):
        r1 = self._register(modes, 1)
        r2 = self._register(modes, 2)
        r3 = self.program[self.ip + 3]
        if modes[3] == 2:
            self.program[self.relative_base + self.program[self.ip + 3]] = r1 + r2
        else:
            self.program[r3] = r1 + r2
        self._ternary_increment()
    

    def _mult(self, modes):
        r1 = self._register(modes, 1)
        r2 = self._register(modes, 2)
        r3 = self.program[self.ip + 3]
        if modes[3] == 2:
            self.program[self.relative_base + self.program[self.ip + 3]] = r1 * r2
        else:
            self.program[r3] = r1 * r2
        self._ternary_increment()
    

    def _save(self, modes):
        if modes[1] == 2:
            self.program[self.relative_base + self.program[self.ip + 1]] = self._get_input()
        else:
            self.program[self.program[self.ip + 1]] = self._get_input()
        self._unary_increment()
    

    def _iden(self, modes):
        r1 = self._register(modes, 1)
        self.output(r1)
        self._unary_increment()
    

    def _jit(self, modes):
        r1 = self._register(modes, 1)
        r2 = self._register(modes, 2)

        if r1 != 0:
            self.ip = r2
        else:
            self._binary_increment()

    
    def _jif(self, modes):
        r1 = self._register(modes, 1)
        r2 = self._register(modes, 2)
        if r1 == 0:
            self.ip = r2
        else:
            self.ip = (self.ip + 3)

    
    def _lt(self, modes):
        r1 = self._register(modes, 1)
        r2 = self._register(modes, 2)
        r3 = self.program[self.ip + 3]

        if modes[3] == 2:
            r3 = self.relative_base + self.program[self.ip + 3]

        if r1 < r2:
            self.program[r3] = 1
        else:
            self.program[r3] = 0
        self._ternary_increment()
    

    def _eq(self, modes):
        r1 = self._register(modes, 1)
        r2 = self._register(modes, 2)
        r3 = self.program[self.ip + 3]

        if modes[3] == 2:
            r3 = self.relative_base + self.program[self.ip + 3]

        if r1 == r2:
            self.program[r3] = 1
        else:
            self.program[r3] = 0
        self._ternary_increment()


    def _rb(self, modes):
        r1 = self._register(modes, 1)
        self.relative_base = self.relative_base + r1
        self._unary_increment()


    def _unary_increment(self):
        self.ip = (self.ip + 2)


    def _binary_increment(self):
        self.ip = (self.ip + 3)


    def _ternary_increment(self):
        self.ip = (self.ip + 4)
