# calculator/tests.py

import unittest
from pkg.calculator import Calculator
import math

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    # --- Basic arithmetic ---
    def test_addition(self):
        self.assertEqual(self.calc.evaluate("3+5"), 8)

    def test_subtraction(self):
        self.assertEqual(self.calc.evaluate("10-4"), 6)

    def test_multiplication(self):
        self.assertEqual(self.calc.evaluate("3*4"), 12)

    def test_division(self):
        self.assertEqual(self.calc.evaluate("10/2"), 5)

    def test_nested_expression(self):
        self.assertEqual(self.calc.evaluate("3*4+5"), 17)

    def test_complex_expression(self):
        self.assertEqual(self.calc.evaluate("2*3-8/2+5"), 7)

    # --- Scientific functions ---
    def test_power(self):
        self.assertEqual(self.calc.evaluate("2^3"), 8)
        self.assertEqual(self.calc.evaluate("5 ^ 0"), 1)

    def test_root(self):
        self.assertEqual(self.calc.evaluate("root(2,16)"), 4)
        self.assertEqual(self.calc.evaluate("root(3,27)"), 3)
    
        self.assertAlmostEqual(self.calc.evaluate("root(2,0.25)"), 0.5)

        with self.assertRaises(ValueError): 
            self.calc.evaluate("root(2,-16)")
            
            
    def test_log(self):
        self.assertAlmostEqual(self.calc.evaluate("log(100)"), 2)
        
    def test_ln(self):
        self.assertAlmostEqual(self.calc.evaluate("ln(e)"), 1)
        
    def test_factorial(self):
        self.assertEqual(self.calc.evaluate("5!"), 120)

    def test_inverse(self):
        self.assertAlmostEqual(self.calc.evaluate("inv(4)"), 0.25)    

    def test_trig_sin_deg(self):
        self.calc.set_mode("deg")
        self.assertAlmostEqual(self.calc.evaluate("sin(90)"), 1, places=5)

    def test_trig_cos_rad(self):
        self.calc.set_mode("rad")
        self.assertAlmostEqual(self.calc.evaluate("cos(pi)"), -1, places=5)
    
    def test_hyperbolic_functions(self):
        expression = "sinh(1) + cosh(1) - tanh(1)"
        expected_result = math.sinh(1) + math.cosh(1) - math.tanh(1)
        self.assertAlmostEqual(self.calc.evaluate(expression), expected_result, places=5)

    def test_constants(self):
        self.assertAlmostEqual(self.calc.evaluate("2*pi"), 2 * math.pi)
         
    # --- complex test case
    def test_complex_scientific_expression_1(self):
        self.calc.set_mode("deg") 
        expression = "5 + 3*2 - 4/2 + 2^3 + root(3,27) + sin(30) + cos(60) + log(100) + ln(e) + 5!"
        # 5 + 6 - 2 + 8 + 3 + 0.5 + 0.5 + 2 + 1 + 120 = 144
        self.assertAlmostEqual(self.calc.evaluate(expression), 144, places=5)

    def test_complex_expression_2(self):
        self.calc.set_mode("deg")
        expression = "2^3 + root(2,16) + 3!*sin(90) - log(1000) + ln(e^2) + cos(180) + inv(4)"
        # Step-by-step expected:
        # 2^3 = 8
        # root(2,16) = 4
        # 3!*sin(90) = 6*1 = 6
        # -log(1000) = -3
        # ln(e^2) = 2
        # cos(180 deg) = -1
        # inv(4) = 0.25
        # Total = 8 + 4 + 6 - 3 + 2 - 1 + 0.25 = 16.25
        expected_result = 16.25
        self.assertAlmostEqual(self.calc.evaluate(expression), expected_result, places=5)

    def test_complex_expression_3(self):
        self.calc.set_mode("rad")
        expression = "5!*2^3 + root(4,16) - pi + cos(pi/2) + ln(e^3) + inv(2)"
        # Step-by-step:
        # 5! = 120
        # 120*2^3 = 120*8 = 960
        # root(4,16) = 2
        # -pi ≈ -3.141592653589793
        # cos(pi/2) ≈ 0
        # ln(e^3) = 3
        # inv(2) = 0.5
        # Total ≈ 960 + 2 - 3.141592653589793 + 0 + 3 + 0.5 ≈ 962.3584073464102
        expected_result = 962.3584073464102
        self.assertAlmostEqual(self.calc.evaluate(expression), expected_result, places=5)

    def test_complex_expression_4(self):
        self.calc.set_mode("deg")
        expression = "2^4 + root(2,64) + 4!*sin(30) + cos(60) + log(100) - inv(5) + ln(e)"
        # Step-by-step:
        # 2^4 = 16
        # root(2,64) = 8
        # 4!*sin(30) = 24*0.5 = 12
        # cos(60) = 0.5
        # log(100) = 2
        # -inv(5) = -0.2
        # ln(e) = 1
        # Total = 16 + 8 + 12 + 0.5 + 2 - 0.2 + 1 = 39.3
        expected_result = 39.3
        self.assertAlmostEqual(self.calc.evaluate(expression), expected_result, places=5)

    def test_complex_scientific_expression_finalboss(self):
        self.calc.set_mode("rad")
        expression = (
        "2^3 + sqrt(16) - log(100) + ln(e) + 5! + "
        "sinh(1) + cosh(1) - tanh(1) + sin(90) + cos(pi) + 2*pi"
        )
        
        self.assertAlmostEqual(self.calc.evaluate(expression), 139.13386964328342, places=5)
        
    # --- Edge cases & errors ---
    def test_empty_expression(self):
        self.assertIsNone(self.calc.evaluate(""))

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calc.evaluate("$3+5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calc.evaluate("3+")


if __name__ == "__main__":
    unittest.main()
