# ast.py
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Number:
    """
    Node for numerical values (real or complex)
    """

    value: complex


@dataclass(frozen=True)
class Variable:
    """
    Node for symbolic variables
    """

    name: str


@dataclass(frozen=True)
class UnaryOp:
    """
    Node for unary operations
    """

    op: str
    operand: "AST"


@dataclass(frozen=True)
class BinaryOp:
    """
    Node for binary operations
    """

    op: str
    left: "AST"
    right: "AST"


# Generic AST type
AST = Union[Number, Variable, UnaryOp, BinaryOp]
