import re  # Regular expression module
from typing import List, TypedDict, Literal


class OperatorInfo(TypedDict):
    """
    - prec: precedence (integer)
    - assoc: associativity ('L' left, 'R' right)
    """

    prec: int
    assoc: Literal["L", "R"]


# Shunting-Yard based
_OPERATORS: dict[str, OperatorInfo] = {
    "+": {"prec": 1, "assoc": "L"},
    "-": {"prec": 1, "assoc": "L"},
    "*": {"prec": 2, "assoc": "L"},
    "/": {"prec": 2, "assoc": "L"},
    "^": {"prec": 3, "assoc": "R"},
}

# \s* ignores blankspaces
# matches 1 of 3 groups:
#   integer or decimal numer
#   variable (letter followed by either letter or digits)
#   operators or parenthesis
_TOKEN_REGEX = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([A-Za-z]\w*)|([\+\-\*/\^\(\)]))")


def tokenize(expr: str) -> List[str]:
    """
    expr (ex. '2*x + 3') -> tokens list: ['2', '*', 'x', '+', '3'].

    Parameters:
        expr: str with the expr.
    Returns:
        substrings List (tokens).
    Exceptions:
        ValueError for invalid characters.
    """
    tokens: List[str] = []
    idx: int = 0
    while idx < len(expr):
        match = _TOKEN_REGEX.match(expr, idx)
        if not match:  # if match fails, then match is None
            raise ValueError(f"Invalid token in position {idx}: '{expr[idx:]}'")
        num, var, op = match.groups()
        if num:
            tokens.append(num)
        elif var:
            tokens.append(var)
        elif op:
            tokens.append(op)
        idx = match.end()
    return tokens


def to_rpn(tokens: List[str]) -> List[str]:
    """
    Transforms the tokens list from infix to reverse polish notation (RPN) using the Shunting‑Yard algorithm.

    Parameters:
        tokens: tokens list in infix notation.
    Returns:
        RPN list.
    Exceptions:
        ValueError there are unbalanced parenthesis or unexpected tokens.
    """
    output: List[str] = []
    operator_stack: List[str] = []

    for token in tokens:
        # numbers and variables go directly to the output
        if token not in _OPERATORS and token not in ("(", ")"):
            output.append(token)
        elif token in _OPERATORS:
            while operator_stack and operator_stack[-1] in _OPERATORS:
                top = operator_stack[-1]
                curr = _OPERATORS[token]
                prev = _OPERATORS[top]
                if (curr["assoc"] == "L" and curr["prec"] <= prev["prec"]) or (
                    curr["assoc"] == "R" and curr["prec"] < prev["prec"]
                ):
                    output.append(operator_stack.pop())
                else:
                    break
            operator_stack.append(token)
        elif token == "(":
            operator_stack.append(token)
        elif token == ")":
            while operator_stack and operator_stack[-1] != "(":
                output.append(operator_stack.pop())
            if not operator_stack or operator_stack[-1] != "(":
                raise ValueError("Unbalanced parenthesis")
            operator_stack.pop()
        else:
            raise ValueError(f"Unexpected token: {token}")
    while operator_stack:
        top = operator_stack.pop()
        if top in ("(", ")"):
            raise ValueError("Unbalanced parenthesis")
        output.append(top)
    return output
