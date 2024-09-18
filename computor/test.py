import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from computor.computorv2 import computorv2

class TestComputorv2(unittest.TestCase):
    def setUp(self):
        pass
    
    def  computor(self, user_input):
        return computorv2(user_input, False)
    
    def tearDown(self):
        pass

    def test_preliminary_checks(self):
        # Test natural integers
        self.assertEqual(self.computor("x = 42"), 42)
        
        # Test rational numbers
        self.assertEqual(self.computor("y = 3/4"), 0.75)
        
        # Test complex numbers
        self.assertEqual(str(self.computor("z = 2 + 3j")), "(2+3j)")
        
        # Test matrices
        self.assertEqual(str(self.computor("A = [[1,2];[3,4]]")), "[[1, 2], [3, 4]]")
        
        # Test polynomial equations
        self.assertEqual(str(self.computor("f(x) = x ^ 2 + 2 * x + 1")), "x ^ 2 + 2 * x + 1")

    # ------------------ TESTS ------------------ #

    def test_basic_assignment(self):
        self.assertEqual(self.computor("varA = 2"), 2)
        self.assertEqual(self.computor("varB = 4"), 4)
        self.assertEqual(self.computor("varC = -2"), -2)
        self.assertEqual(self.computor("2 + 4"), 6)
        self.assertEqual(self.computor("4 - 2"), 2)
        self.assertEqual(self.computor("4 * 2"), 8)
        self.assertEqual(self.computor("4 / 2"), 2)
        self.assertEqual(self.computor("4 % 2"), 0)
        self.assertEqual(self.computor("4 ^ 2"), 16)
        self.assertEqual(self.computor(" 2 + -4"), -2)
        self.assertEqual(self.computor(" 2 - -4"), 6)
        self.assertEqual(self.computor(" 2 * -4"), -8)
        self.assertEqual(self.computor(" 2 / -4"), -0.5)
        self.assertEqual(self.computor(" 2 % -4"), -2)
        self.assertEqual(self.computor(" 2 ^ -4"), 0.0625)
   
    def test_unary_operations(self):
        self.assertEqual(self.computor("2 + -4"), -2)
        self.assertEqual(self.computor("2 - -4"), 6)
        self.assertEqual(self.computor("2 * -4"), -8)
        self.assertEqual(self.computor("2 / -4"), -0.5)
        self.assertEqual(self.computor("2 % -4"), -2)
        self.assertEqual(self.computor("2 ^ -4"), 0.0625)
        
    def test_rational_assignment(self):
        self.assertEqual(self.computor("varA = 2"), 2)
        self.assertEqual(self.computor("varB = 4.242"), 4.242)
        self.assertEqual(self.computor("varC = -4.3"), -4.3)
        self.assertEqual(self.computor("varD = 2.3 + 4.2"), 6.5)
        self.assertEqual(self.computor("varE = -4.2 - 4.2"), -8.4)
        self.assertEqual(self.computor("varE = 1 / 3 - 2"), (1 / 3 - 2))
        self.assertEqual(self.computor("varE = 1 / 3 + 2"), (1 / 3 + 2))
        self.assertEqual(self.computor("varE = 1 / 3 * 2"), (1 / 3 * 2))
        self.assertEqual(self.computor("varE = 1 / 3 / 2"), (1 / 3 / 2))
        self.assertEqual(self.computor("varE = 1 / 3 ^ 2"), (1 / 3 ** 2))
        self.assertEqual(self.computor("varE = 1 / 3 ^ 2 + 2"), (1 / 3 ** 2 + 2))
        self.assertEqual(self.computor("varE = 1 / 3 ^ 2 - 2"), (1 / 3 ** 2 - 2))
        self.assertEqual(self.computor("varE = 1 / 3 ^ 2 * 2"), (1 / 3 ** 2 * 2))
        self.assertEqual(self.computor("varE = 1 / 3 ^ 2 / 2"), (1 / 3 ** 2 / 2))
        self.assertEqual(self.computor("varE = 1 / 3 ^ 2 ^ 2"), (1 / 3 ** 2 ** 2))
        self.assertEqual(self.computor("varE = 1 / 3 ^ 2 ^ 2 + 2"), (1 / 3 ** 2 ** 2 + 2))
        self.assertEqual(self.computor("varE = 1 / 3 ^ 2 ^ 2 - 2"), (1 / 3 ** 2 ** 2 - 2))
        self.assertEqual(self.computor("varE = 1 / 3 ^ 2 ^ 2 * 2"), (1 / 3 ** 2 ** 2 * 2))
        self.assertEqual(self.computor("varE = 1 / 3 ^ 2 ^ 2 / 2"), (1 / 3 ** 2 ** 2 / 2))
        self.assertEqual(self.computor("varE = 1 / 3 ^ 2 ^ 2 ^ 2"), (1 / 3 ** 2 ** 2 ** 2))

    def test_variable_reassignment(self):
        self.computor("x = 2")
        self.assertEqual(self.computor("y = x"), 2)
        self.assertEqual(self.computor("y = 7"), 7)
        self.assertEqual((self.computor("y = 2 * 3 - 4")), 2)
    
    def test_computation_assignment(self):
        self.assertEqual(self.computor("varA =  2 - 5"), ( 2 - 5))
        self.assertEqual(self.computor("varB = 2 * varA - 5 %4"), (2 * (2 - 5) - 5 %4))

    def test_basic_arithmetic(self):
        self.assertEqual(self.computor("2 + 3 * 4 - 5 / 2 ?"), 11.5)
        self.assertEqual(self.computor("10 % 3 ?"), 1)

    def test_error_handling(self):
        with self.assertRaises(ValueError):
            self.computor("5 / 0")
        pass

    def test_case_insensitivity(self):
        self.computor("vara = 5")
        self.assertEqual(self.computor("vara + 3 ?"), 8)

    def test_power_operations(self):
        self.assertEqual(self.computor("2^3 ?"), 8)
        self.assertEqual(self.computor("-2^2 ?"), 4)

    def test_parentheses(self):
        self.assertEqual(self.computor("(2 + 3) * 4"), 20)
        self.assertEqual(self.computor("2 + 3 * (4 - 5) ?"), -1)
        self.assertEqual(self.computor("2 * (3 + 4) ?"), 14)
        self.assertEqual(self.computor("2 * (3 + 4) / 2 ?"), 7)
        self.assertEqual(self.computor("2 * (3 + 4) / 2 + 3 ?"), 10)
        self.assertEqual(self.computor("2 * (3 + 4) / 2 + 3 * 2 - 4 / 2 ?"), 11)
        self.assertEqual(self.computor("2 * (3 + 4) / 2 + 3 * 2 - 4 / 2 ^ 2 ?"), 12)
    
    def test_complex_assignment(self):
        self.assertEqual(str(self.computor("varD = 2j + 3")), "(3+2j)")
        self.assertEqual(str(self.computor("varE = -4j - 4")), "(-4-4j)")
        pass
    
    def test_matrix_assignment(self):
        self.assertEqual((self.computor("matA = [[2,3];[4,3]]")), [[2,3],[4,3]])
        self.assertEqual((self.computor("matB = [[3,4]]")), [[3, 4]])
        self.assertEqual((self.computor("matC = [[2,3,4];[4,3,2];[1,2,3]]")), [[2,3,4],[4,3,2],[1,2,3]])
      
    def test_matrix_errors(self):
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3];[1,2,5]]")
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3]:[1,2]]")
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3] + 2]")
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3] - 2]")

    def test_matrix_operations(self):
        self.assertEqual((self.computor("matD = [[2,3,4];[4,3,2];[1,2,3]] + [[2,3,4];[4,3,2];[1,2,3]]")), [[4,6,8],[8,6,4],[2,4,6]])
        self.assertEqual((self.computor("matE = [[2,3,4];[4,3,2];[1,2,3]] - [[2,3,4];[4,3,2];[1,2,3]]")), [[0,0,0],[0,0,0],[0,0,0]])
        self.assertEqual((self.computor("matF = [[2,3,4];[4,3,2];[1,2,3]] * [[2,3,4];[4,3,2];[1,2,3]]")), [[20, 23, 26], [22, 25, 28], [13, 15, 17]])
        self.assertEqual((self.computor("matG = [[2,3,4];[4,3,2];[1,2,3]] / [[2,3,4];[4,3,2];[1,2,3]]")), [[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        self.assertEqual((self.computor("matH = [[2,3,4];[4,3,2];[1,2,3]] % [[2,3,4];[4,3,2];[1,2,3]]")), [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def test_scalar_matrix_operations(self):
        self.assertEqual((self.computor("matA = [[2,3];[4,3]] + 2")), [[4,5],[6,5]])
        self.assertEqual((self.computor("matB = [[2,3];[4,3]] - 2")), [[0,1],[2,1]])
        self.assertEqual((self.computor("matC = [[2,3];[4,3]] * 2")), [[4,6],[8,6]])
        self.assertEqual((self.computor("matD = [[2,3];[4,3]] / 2")), [[1,1.5],[2,1.5]])
        self.assertEqual((self.computor("matE = [[2,3];[4,3]] % 2")), [[0,1],[0,1]])

    def test_matrix_operation_errors(self):
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3]] + [[2,3,5];[4,3]]")
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3]] - [[2,3,5];[4,3]]")
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3]] * [[2,3,5];[4,3]]")
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3]] / [[2,3,5];[4,3]]")
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3]] % [[2,3,5];[4,3]]")
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3]] + 2j")
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3]] - 2j")
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3]] * 2j")
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3]] / 2j")
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3]] % 2j")
        with self.assertRaises(ValueError):
            self.computor("matA = [[2,3];[4,3]] + [2,3]")

    def test_function_assignment(self):
        self.assertEqual(str(self.computor("funA(x) = 2 * x  ^ 5 + 4 * x ^ 2 - 5 * x + 4")), "2 * x ^ 5 + 4 * x ^ 2 - 5 * x + 4")
        self.assertEqual(str(self.computor("funB(y) = 43 * y / (4 % 2 * y)")), "43 * y / ( 4 % 2 * y )")
        self.assertEqual(str(self.computor("funC(z) = 2 * z + 3")), "2 * z + 3")

    def test_matrix_operations2(self):
        self.computor("matA = [[1,2];[3,4]]")
        self.computor("matB = [[5,6];[7,8]]")
        self.assertEqual(str(self.computor("matA * matB ?")), "[[19, 22], [43, 50]]")
        self.assertEqual(str(self.computor("2 * matA ?")), "[[2, 4], [6, 8]]")

    def test_function_evaluation(self):
        self.assertEqual(self.computor("A(x) = 2 * 4 + x"), "2 * 4 + x")
        self.computor("B(x) = 4 -5 + (x + 2)^2 - 4")
        self.assertEqual(self.computor("A(2) + B(4) ?"), 41)
        self.assertEqual(self.computor("A(2) + B(4) + 2 ?"), 43)
        self.assertEqual(self.computor("A(2) - B(4) ?"), -21)
        self.assertEqual(self.computor("A(2) * B(4) ?"), 310)
        self.assertEqual(self.computor("A(2) / B(4) ?"), 0.3225806451612903)
        self.assertEqual(self.computor("A(2) % B(4) ?"), 10)

    def test_equation_solving(self):
        self.computor("funD(x) = x + 1")
        self.computor("y = 0")
        self.assertEqual(self.computor("funD(x) = 12"), "12")
        self.computor("A(x) = x * 2 + 3 - x ^ 2 ")
        self.assertEqual(self.computor("A(x) = 10 + x"), "10 + x")

if __name__ == '__main__':
    unittest.main()