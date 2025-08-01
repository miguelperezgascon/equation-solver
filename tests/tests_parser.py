# tests/tests_parser.py
import pytest
from src.parser import tokenize, to_rpn, parse_rpn, parse
from src.ast import Number, Variable, UnaryOp, BinaryOp


@pytest.mark.parametrize(
    "expr,tokens",
    [
        ("3*x+sin(x)", ["3", "*", "x", "+", "sin", "(", "x", ")"]),
        ("2.5+4", ["2.5", "+", "4"]),
    ],
)
def test_tokenize(expr, tokens):
    assert tokenize(expr) == tokens


@pytest.mark.parametrize(
    "tokens,rpn",
    [
        (["3", "*", "x", "+", "4"], ["3", "x", "*", "4", "+"]),
        (["x", "^", "2"], ["x", "2", "^"]),
    ],
)
def test_to_rpn(tokens, rpn):
    assert to_rpn(tokens) == rpn


@pytest.mark.parametrize(
    "rpn,ast_type",
    [
        (["3", "x", "*"], BinaryOp),
        (["x", "sin"], UnaryOp),  # intentionally invalid? adjust
    ],
)
def test_parse_rpn(rpn, ast_type):
    ast = parse_rpn(rpn)
    assert isinstance(ast, ast_type)


@pytest.mark.parametrize(
    "expr",
    [
        "x+1=0",
        "sin(x)-x=0",
    ],
)
def test_parse(expr):
    lhs, rhs = parse(expr)
    # ensure ASTs returned
    assert lhs is not None
    assert rhs is not None
