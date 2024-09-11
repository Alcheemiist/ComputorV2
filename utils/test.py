import unittest
from main import Computorv2  # Assuming the main class is named Computorv2

class TestComputorv2(unittest.TestCase):
    def setUp(self):
        self.computor = Computorv2()

    def test_rational_assignment(self):
        self.assertEqual(self.computor.process("varA = 2"), 2)
        self.assertEqual(self.computor.process("varB = 4.242"), 4.242)
        self.assertEqual(self.computor.process("varC = -4.3"), -4.3)

    def test_complex_assignment(self):
        self.assertEqual(str(self.computor.process("varD = 2*i + 3")), "3 + 2i")
        self.assertEqual(str(self.computor.process("varE = -4i - 4")), "-4 - 4i")

    def test_matrix_assignment(self):
        self.assertEqual(str(self.computor.process("matA = [[2,3];[4,3]]")), "[ 2 , 3 ]\n[ 4 , 3 ]")
        self.assertEqual(str(self.computor.process("matB = [[3,4]]")), "[ 3 , 4 ]")

    def test_function_assignment(self):
        self.assertEqual(str(self.computor.process("funA(x) = 2*x^5 + 4x^2 - 5*x + 4")), "2 * x^5 + 4 * x^2 - 5*x + 4")
        self.assertEqual(str(self.computor.process("funB(y) = 43 * y / (4 % 2 * y)")), "43 * y / (4 % 2 * y)")

    def test_variable_reassignment(self):
        self.computor.process("x = 2")
        self.assertEqual(self.computor.process("y = x"), 2)
        self.assertEqual(self.computor.process("y = 7"), 7)
        self.assertEqual(str(self.computor.process("y = 2 * i - 4")), "-4 + 2i")

    def test_computation_assignment(self):
        self.assertEqual(self.computor.process("varA = 2 + 4 *2 - 5 %4 + 2 * (4 + 5)"), 27)
        self.assertEqual(self.computor.process("varB = 2 * varA - 5 %4"), 53)

    def test_basic_arithmetic(self):
        self.assertEqual(self.computor.process("2 + 3 * 4 - 5 / 2 ?"), 11.5)
        self.assertEqual(self.computor.process("10 % 3 ?"), 1)

    def test_matrix_operations(self):
        self.computor.process("matA = [[1,2];[3,4]]")
        self.computor.process("matB = [[5,6];[7,8]]")
        self.assertEqual(str(self.computor.process("matA * matB ?")), "[ 19 , 22 ]\n[ 43 , 50 ]")
        self.assertEqual(str(self.computor.process("2 * matA ?")), "[ 2 , 4 ]\n[ 6 , 8 ]")

    def test_power_operations(self):
        self.assertEqual(self.computor.process("2^3 ?"), 8)
        self.assertEqual(self.computor.process("-2^2 ?"), -4)  # This tests if the program respects the convention that exponentiation has higher precedence than unary minus

    def test_function_evaluation(self):
        self.computor.process("funA(x) = 2 * 4 + x")
        self.computor.process("funB(x) = 4 -5 + (x + 2)^2 - 4")
        self.assertEqual(self.computor.process("funA(2) + funB(4) ?"), 41)

    def test_equation_solving(self):
        self.computor.process("funD(x) = x^2 + 2x + 1")
        self.computor.process("y = 0")
        self.assertEqual(self.computor.process("funD(x) = y ?"), "x^2 + 2x + 1 = 0\nUne solution sur R :\n-1")

    def test_error_handling(self):
        with self.assertRaises(ValueError):
            self.computor.process("5 / 0 ?")

    def test_case_insensitivity(self):
        self.computor.process("VarA = 5")
        self.assertEqual(self.computor.process("vara + 3 ?"), 8)

if __name__ == '__main__':
    unittest.main()