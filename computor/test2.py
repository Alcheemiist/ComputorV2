import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from computor.computorv2 import computorv2

class TestComputorv2(unittest.TestCase):
    def computor(self, user_input):
        return computorv2(user_input, False)
    
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

    def test_assignment_errors(self):
        # Elementary errors

        with self.assertRaises(Exception):
            self.computor("x == 2")

        with self.assertRaises(Exception):
            self.computor("x = 2 = 3")
        
        # with self.assertRaises(Exception):
        #     self.computor("x = 23edd23-+-+")
        
        # Semi-advanced errors
        with self.assertRaises(Exception):
            self.computor("= 2")
        with self.assertRaises(Exception):
            self.computor("3 = 4")
        with self.assertRaises(Exception):
            self.computor("x = g")  # Assuming g is not defined
        
        # Advanced errors
        # self.assertNotEqual(self.computor("x = --2"), 2)  # This should be handled as an error or as 2
        # with self.assertRaises(Exception):
        #     self.computor("f(x) = x * 2")
        #     self.computor("t = f(x)")  # This should raise an error as x is not defined
        # with self.assertRaises(Exception):
        #     self.computor("i = 2")  # i should not be assignable

    def test_valid_assignments(self):
        # Elementary assignments
        self.assertEqual(self.computor("x = 2"), 2)
        # self.assertEqual(str(self.computor("y = 4i")), "4i")
        # self.assertEqual(str(self.computor("z = [[2,3];[3,5]]")), "[[2, 3], [3, 5]]")
        
        # Semi-advanced assignments
        self.computor("x = 2")
        self.assertEqual(self.computor("y = x"), 2)
        self.computor("x = 5")
        self.assertEqual(self.computor("x"), 5)
        
        # Advanced assignments
        self.computor("x = 2")
        # self.computor("y = x * [[4,2]]")
        # self.computor("f(z) = z * y")
        # self.assertEqual(str(self.computor("f(z)")), "z * [[8, 4]]")

    def test_calculations(self):
        # Elementary calculations
        self.assertEqual(self.computor("2 + 2"), 4)
        self.assertEqual(self.computor("3 * 4"), 12)
        with self.assertRaises(Exception):
            self.computor("2 / 0")
        self.assertEqual(self.computor("1.5 + 1"), 2.5)
        
        # Semi-advanced calculations
        # self.computor("x = 2 * i")
        # self.assertEqual(str(self.computor("x ^ 2")), "-4")


        # self.computor("A = [[2,3];[3,4]]")
        # self.computor("B = [[1,0];[0,1]]")
        # self.assertEqual(str(self.computor("A ** B")), "[[2, 3], [3, 4]]")
        
        # # Advanced calculations
        # self.assertEqual(self.computor("4 - 3 - ( 2 * 3 ) ^ 2 * ( 2 - 4 ) + 4"), 76)
        # self.computor("f(x) = 2*(x + 3*(x - 4))")
        # self.computor("p = 2")
        # self.assertEqual(self.computor("f(3) - f(p) + 2"), 10)

if __name__ == '__main__':
    unittest.main()