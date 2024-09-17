import unittest
from computorv1 import computorv1

class TestComputorV1(unittest.TestCase):


    def test_case_1(self):
        result = computorv1("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
        self.assertAlmostEqual(result[0], -0.475131, places=5)
        self.assertAlmostEqual(result[1], 0.905239, places=5)

    def test_case_2(self):
        result = computorv1("5 * X^0 + 4 * X^1 = 4 * X^0")
        self.assertAlmostEqual(result[0], -0.25)

    def test_case_3(self):
        result = computorv1("8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0")
        self.assertEqual(result[0], "The polynomial degree is strictly greater than 2, I can't solve.")

  
    def test_case_5(self):
        result = computorv1("1 * X^2 + X^1 = 1 * X^2")
        self.assertEqual(result[0], "No solution.")


if __name__ == '__main__':
    unittest.main()