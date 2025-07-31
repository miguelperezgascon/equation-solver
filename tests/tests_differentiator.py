# tests/test_differentiator.py
import pytest
from src.ast import Number, Variable, UnaryOp, BinaryOp
from src.differentiator import diff_ast


# d/dx [x^2] = 2*x
def test_diff_square(self):
    # d/dx [x^2] = 2 * x
    ast = BinaryOp("^", Variable("x"), Number(2))
    d = diff_ast(ast, "x")
    # Expect top-level BinaryOp('*', Number(2), x^1)
    self.assertIsInstance(d, BinaryOp)
    self.assertEqual(d.op, "*")
    # Left operand should be 2
    self.assertIsInstance(d.left, Number)
    self.assertEqual(d.left.value, 2)
    # Right operand should be x^1
    right = d.right
    self.assertIsInstance(right, BinaryOp)
    self.assertEqual(right.op, "^")
    # Check base is x and exponent is 1
    self.assertIsInstance(right.left, Variable)
    self.assertEqual(right.left.name, "x")
    self.assertIsInstance(right.right, Number)
    self.assertEqual(right.right.value, 1)
