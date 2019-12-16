import os
import sys
import robot
sys.path.insert(0, os.path.abspath('../intcode'))
import intcode

r = robot.Robot(starting_panel=1)

def handle_output(output):
    global r
    color, direction = output
    r.move(color, direction)

with open('input') as f:
    program = [int(s) for s in f.read().split(',')]
    brain = intcode.IntCode(program, observer=handle_output, driver=r.access_camera, output_step=2)
    brain.execute()

    upper_x = max(r.painted, key=lambda point: point.x).x
    lower_x = min(r.painted, key=lambda point: point.x).x
    upper_y = max(r.painted, key=lambda point: point.y).y
    lower_y = min(r.painted, key=lambda point: point.y).y

    for y in range(lower_y, upper_y + 1):
        for x in range(lower_x, upper_x + 1):
            point =  robot.Position(x=x, y=y)
            color = r.painted[point]
            if color == 1:
                print('#', end='')
            else:
                print('.', end='')
        print()
