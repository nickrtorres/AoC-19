import intcode

with open('input') as f:
    input = [int(i) for i in f.read().split(',')]

computer = intcode.IntCode(input, print)
computer.input_register = 2
computer.execute()
