# tests/tests_evaluator.py
import pytest
import cmath
from src.ast import Number, Variable, UnaryOp, BinaryOp
from src.evaluator import eval_ast


# AST: 3
def test_eval_number():
    assert eval_ast(Number(3 + 0j), {}, "x") == 3 + 0j


# AST: x
def test_eval_variable():
    assert eval_ast(Variable("x"), {"x": 2 + 0j}, "x") == 2 + 0j


# AST: sin(x)
def test_eval_sin():
    ast = UnaryOp("sin", Variable("x"))
    val = eval_ast(ast, {"x": cmath.pi / 2}, "x")
    assert abs(val - 1) < 1e-8


# AST: x^2 + 1
def test_eval_binary():
    ast = BinaryOp("+", BinaryOp("^", Variable("x"), Number(2)), Number(1))
    assert eval_ast(ast, {"x": 3}, "x") == 10
