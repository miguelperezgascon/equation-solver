# parser.py
import re
from typing import List, Tuple
from src.ast import AST, Number, Variable, UnaryOp, BinaryOp


def tokenize(expr: str) -> List[str]:
    token_pattern = r"\d+\.\d+|\d+|[A-Za-z_]+|[+\-*/^=()]"
    return re.findall(token_pattern, expr)


def to_rpn(tokens: List[str]) -> List[str]:
    prec: dict[str, int] = {"+": 2, "-": 2, "*": 3, "/": 3, "^": 4}
    right_assoc: set[str] = {"^"}
    output: List[str] = []
    op_stack: List[str] = []

    pattern = re.compile(r"^(?:\d+\.?\d*|[A-Za-z_]+)$")

    for token in tokens:
        if re.match(pattern, token):
            output.append(token)
        elif token == "(":
            op_stack.append(token)
        elif token == ")":
            while op_stack and op_stack[-1] != "(":
                output.append(op_stack.pop())
            if not op_stack or op_stack[-1] != "(":
                raise ValueError("Unbalanced parenthesis")
            op_stack.pop()
        else:
            while (
                op_stack
                and op_stack[-1] != "("
                and (
                    (prec.get(op_stack[-1], 0), token not in right_assoc)
                    > (prec.get(token, 0), False)
                )
            ):
                output.append(op_stack.pop())
            op_stack.append(token)

    while op_stack:
        output.append(op_stack.pop())
    return output


def parse_rpn(rpn: List[str]) -> AST:
    stack: List[AST] = []

    pattern_num = re.compile(r"^\d+\.?\d*$")
    pattern_var = re.compile(r"^[A-Za-z_]+$")

    for token in rpn:
        if re.match(pattern_num, token):
            stack.append(Number(complex(token)))
        elif re.match(pattern_var, token):
            if token in ("sin", "cos", "tan", "neg"):
                operand = stack.pop()
                stack.append(UnaryOp(token, operand))
            else:
                stack.append(Variable(token))
        else:
            right = stack.pop()
            left = stack.pop()
            stack.append(BinaryOp(token, left, right))
    return stack[0]


def parse(expr: str) -> Tuple[AST, AST]:
    tokens = tokenize(expr)
    idx = tokens.index("=")
    lhs_tokens = tokens[:idx]
    rhs_tokens = tokens[idx + 1 :]
    lhs_rpn = to_rpn(lhs_tokens)
    rhs_rpn = to_rpn(rhs_tokens)
    return parse_rpn(lhs_rpn), parse_rpn(rhs_rpn)
