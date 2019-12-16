import os
import sys
import robot
sys.path.insert(0, os.path.abspath('../intcode'))
import intcode

r = robot.Robot()

def handle_output(output):
    global r
    color, direction = output
    r.move(color, direction)

with open('input') as f:
    program = [int(s) for s in f.read().split(',')]
    brain = intcode.IntCode(program, observer=handle_output, driver=r.access_camera, output_step=2)
    brain.execute()
    print(len(r.painted))

