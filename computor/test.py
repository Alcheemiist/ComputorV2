import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from computor.computorv2 import computorv2

class TestComputorv2(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_preliminary_checks(self):
        # Test natural integers
        self.assertEqual(self.computor("x = 42"), 42)
        
        # Test rational numbers
        self.assertEqual(self.computor("y = 3/4"), 0.75)
        
        # Test complex numbers
        # self.assertEqual(str(self.computor("z = 2 + 3i")), "2 + 3i")
        
        # Test matrices
        # self.assertEqual(str(self.computor("A = [[1,2];[3,4]]")), "[[1, 2], [3, 4]]")
        
        # Test polynomial equations
        # self.assertEqual(str(self.computor("f(x) = x^2 + 2x + 1")), "x^2 + 2x + 1")


    def  computor(self, user_input):
            return computorv2(user_input, False)
    
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
        self.assertEqual(str(self.computor("matA = [[2,3];[4,3]]")), "[ 2 , 3 ]\n[ 4 , 3 ]")
        self.assertEqual(str(self.computor("matB = [[3,4]]")), "[ 3 , 4 ]")


# NOT IMPLEMENTED YET


   

    # def test_function_assignment(self):
    #     self.assertEqual(str(self.computor("funA(x) = 2*x^5 + 4x^2 - 5*x + 4")), "2 * x^5 + 4 * x^2 - 5*x + 4")
    #     self.assertEqual(str(self.computor("funB(y) = 43 * y / (4 % 2 * y)")), "43 * y / (4 % 2 * y)")

    # def test_matrix_operations(self):
    #     self.computor("matA = [[1,2];[3,4]]")
    #     self.computor("matB = [[5,6];[7,8]]")
    #     self.assertEqual(str(self.computor("matA * matB ?")), "[ 19 , 22 ]\n[ 43 , 50 ]")
    #     self.assertEqual(str(self.computor("2 * matA ?")), "[ 2 , 4 ]\n[ 6 , 8 ]")

    # def test_function_evaluation(self):
    #     self.computor("funA(x) = 2 * 4 + x")
    #     self.computor("funB(x) = 4 -5 + (x + 2)^2 - 4")
    #     self.assertEqual(self.computor("funA(2) + funB(4) ?"), 41)

    # def test_equation_solving(self):
    #     self.computor("funD(x) = x^2 + 2x + 1")
    #     self.computor("y = 0")
    #     self.assertEqual(self.computor("funD(x) = y ?"), "x^2 + 2x + 1 = 0\nUne solution sur R :\n-1")


if __name__ == '__main__':
    unittest.main()