import collections
import math
import os
import sys

Position  = collections.namedtuple('Position', 'x y')

'''
The Intcode program will serve as the brain of the robot. The program uses input instructions to access the robot's camera:
provide 0 if the robot is over a black panel or 1 if the robot is over a white panel. Then, the program will output two values:

- it will output a value indicating the color to paint the panel the robot is over:
    - 0 means to paint the panel black
    - 1 means to paint the panel white.

- it will output a value indicating the direction the robot should turn:
    - 0 means it should turn left 90 degrees
    - 1 means it should turn right 90 degrees.
'''
class Robot:
    _direction_instructions = {
        0: lambda self: self._turn_left(),
        1: lambda self: self._turn_right()
    }

    def __init__(self, starting_panel=0):
        self.position = Position(x=0, y=0)
        self.direction = 90
        self.direction_instruction = 0
        self.paint_instruction = 0
        self.painted = collections.defaultdict(int)
        self.painted[self.position] = starting_panel

    def _paint(self, color):
        self.painted[self.position] = color
        return (self.position, self.painted[self.position])

    def _turn_left(self):
        self.direction = (self.direction + 90) % 360

    def _turn_right(self):
        self.direction = (self.direction - 90) % 360

    def _advance(self):
        self.position = Position(x=(self.position.x + int(math.cos(math.radians(self.direction)))),
                                 y=(self.position.y + int(math.sin(math.radians(self.direction)))))

    def move(self, color, direction):
        painted = self._paint(color)
        self._direction_instructions[direction](self)
        self._advance()

        return painted

    def access_camera(self):
        return self.painted[self.position]
