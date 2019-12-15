import unittest

import intcode


class IntCodeSuite(unittest.TestCase):
    def test_it_can_add_position_mode(self):
        computer = intcode.IntCode([1, 0, 0, 0, 99])
        computer.execute()
        self.assertEqual(computer.program, [2, 0, 0, 0, 99])

    def test_it_can_add_immediate_mode(self):
        computer = intcode.IntCode([1101, 2, 2, 3, 99])
        computer.execute()
        self.assertEqual(computer.program, [1101, 2, 2, 4, 99])

    def test_it_can_multiply_position_mode(self):
        computer = intcode.IntCode([2, 3, 0, 3, 99])
        computer.execute()
        self.assertEqual(computer.program, [2, 3, 0, 6, 99])

    def test_it_can_multiply_immediate_mode(self):
        computer = intcode.IntCode([1102, 3, 4, 3, 99])
        computer.execute()
        self.assertEqual(computer.program, [1102, 3, 4, 12, 99])

    def test_it_can_read_input(self):
        computer = intcode.IntCode([3, 2, 0])
        computer.input_register = 99
        computer.execute()
        self.assertEqual(computer.program, [3, 2, 99])

    def test_it_can_write_output_position_mode(self):
        computer = intcode.IntCode([4, 2, 99])
        computer.execute()
        self.assertEqual(computer.output_register, 99)

    def test_it_can_write_output_immediate_mode(self):
        computer = intcode.IntCode([104, 3, 99])
        computer.execute()
        self.assertEqual(computer.output_register, 3)

    def test_it_can_jump_when_true_position_mode_true(self):
        computer = intcode.IntCode([5, 1, 4, 99, 7, 1, 2, 99])
        computer.execute()
        self.assertEqual(computer.ip, 7)

    def test_it_can_jump_when_true_immediate_mode_false(self):
        computer = intcode.IntCode([105, 0, 4, 99, 7, 1, 2, 99])
        computer.execute()
        self.assertEqual(computer.ip, 3)

    def test_it_can_jump_when_false_immediate_mode_false(self):
        computer = intcode.IntCode([1106, 0, 3, 99, 7, 1, 2, 99])
        computer.execute()
        self.assertEqual(computer.ip, 3)

    def test_it_checks_less_than(self):
        computer = intcode.IntCode([1107, 1, 2, 5, 104, 1, 99])
        computer.execute()
        self.assertEqual(computer.output_register, 1)

    def test_it_checks_not_less_than(self):
        computer = intcode.IntCode([1107, 3, 2, 5, 104, 1, 99])
        computer.execute()
        self.assertEqual(computer.output_register, 0)

    def test_it_checks_eq(self):
        computer = intcode.IntCode([1108, 2, 2, 5, 104, 1, 99])
        computer.execute()
        self.assertEqual(computer.output_register, 1)

    def test_it_checks_not_ne(self):
        computer = intcode.IntCode([1108, 3, 2, 5, 104, 1, 99])
        computer.execute()
        self.assertEqual(computer.output_register, 0)

    def test_it_resets_relative_base(self):
        computer = intcode.IntCode([9, 1, 99])
        computer.execute()
        self.assertEqual(computer.ip, 2)
        self.assertEqual(computer.relative_base, 1)

    def test_it_resets_relative_base_immediate(self):
        computer = intcode.IntCode([109, 12345, 99])
        computer.execute()
        self.assertEqual(computer.ip, 2)
        self.assertEqual(computer.relative_base, 12345)

    def test_it_can_run_programs(self):
        computer = intcode.IntCode([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1])
        computer.input_register = 1
        computer.execute()
        self.assertEqual(computer.output_register, 1)

    def test_it_can_handle_large_numbers(self):
        computer = intcode.IntCode([1102,34915192,34915192,7,4,7,99,0])
        computer.execute()
        self.assertEqual(len(str(computer.output_register)), 16)
        
    def test_it_can_handle_larger_numbers(self):
        computer = intcode.IntCode([104,1125899906842624,99])
        computer.execute()
        self.assertEqual(computer.output_register, 1125899906842624)

    def test_it_can_quine(self):
        input = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

        output = []
        def observer(register):
            output.append(register)

        computer = intcode.IntCode(input, observer)
        computer.execute()
        self.assertEqual(input, output)

    def test_it_can_query_for_input(self):
        input = [3,13,4,13,3,13,4,13,3,13,4,13,99,0]
        
        stock = [ 0 ]
        def driver():
            stock[0] = stock[0] + 1
            return stock[0]
                

        output = []
        def observer(register):
            output.append(register)
        expected = [1, 2, 3]

        computer = intcode.IntCode(input, observer, driver)
        computer.execute()
        self.assertEqual(expected, output)

    '''
    For example, if the relative base is 2000, then after the instruction 109,19, the relative base would be 2019.
    If the next instruction were 204,-34, then the value at address 1985 would be output.
    '''
    def test_it_can_relative(self):
        input = [109, 19, 204, -34, 99] + [0 for _ in range(1985)]
        input[1985] = 123456789
        computer = intcode.IntCode(input)
        computer.relative_base = 2000
        computer.execute()
        self.assertEqual(computer.output_register, input[1985])

if __name__ == '__main__':
    unittest.main()

