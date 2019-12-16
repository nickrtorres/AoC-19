import robot
import unittest

class RobotSuite(unittest.TestCase):
    def test_it_returns_the_painted_panel(self):
        r = robot.Robot()
        actual = r.move(1, 1)
        expected = (robot.Position(x=0, y=0), 1)
        self.assertEqual(actual, expected)

    def test_it_can_turn_left(self):
        r = robot.Robot()
        r.move(1, 0)
        expected_direction = 180
        self.assertEqual(r.direction, expected_direction)

    def test_it_can_turn_right(self):
        r = robot.Robot()
        r.move(1, 1)
        expected_direction = 0
        self.assertEqual(r.direction, expected_direction)

    def test_it_can_look_down(self):
        r = robot.Robot()
        r.move(1, 1)
        self.assertEqual(0, r.access_camera())

    def test_it_knows_where_it_has_been(self):
        r = robot.Robot()
        r.move(1, 0)
        r.move(1, 0)
        r.move(1, 0)
        r.move(1, 0)
        self.assertEqual(1, r.access_camera())

if __name__ == '__main__':
    unittest.main()
