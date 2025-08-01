# tests/test_differentiator.py
import pytest
from src.ast import Number, Variable, UnaryOp, BinaryOp
from src.differentiator import diff_ast


# d/dx [x^2] = 2*x
def test_diff_square():
    # d/dx [x^2] = 2 * x
    ast = BinaryOp("^", Variable("x"), Number(2))
    d = diff_ast(ast, "x")
    # Expect top-level BinaryOp('*', Number(2), x^1)
    assert isinstance(d, BinaryOp)
    assert d.op == "*"
    assert isinstance(d.left, Number)
    assert d.left.value == 2
    right = d.right
    assert isinstance(right, BinaryOp)
    assert right.op == "^"
    assert isinstance(right.left, Variable)
    assert right.left.name == "x"
    assert isinstance(right.right, Number)
    assert right.right.value == 1
