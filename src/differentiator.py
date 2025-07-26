# differentiatior.py
from src.ast import AST, Number, Variable, UnaryOp, BinaryOp


def diff_ast(node: AST, var: str = "s") -> AST:
    match node:
        case Number(_):
            return Number(0)
        case Variable(n) if n == var:
            return Number(1)
        case Variable(_):
            return Number(0)
        case UnaryOp("neg", u):
            return UnaryOp("neg", diff_ast(u, var))
        case UnaryOp("sin", u):
            # (sin u)' = cos(u) * u'
            return BinaryOp("*", UnaryOp("cos", u), diff_ast(u, var))
        case UnaryOp("cos", u):
            # (cos u)' = -sin(u) * u'
            return BinaryOp("*", UnaryOp("neg", UnaryOp("sin", u)), diff_ast(u, var))
        case UnaryOp("tan", u):
            # (tan u)' = (1 + tan(u)^2) * u'
            tan_u = UnaryOp("tan", u)
            inner = BinaryOp("+", Number(1), BinaryOp("^", tan_u, Number(2)))
            return BinaryOp("*", inner, diff_ast(u, var))
        case BinaryOp("+", a, b):
            return BinaryOp("+", diff_ast(a, var), diff_ast(b, var))
        case BinaryOp("-", a, b):
            return BinaryOp("-", diff_ast(a, var), diff_ast(b, var))
        case BinaryOp("*", a, b):
            # (a*b)' = a'*b + a*b'
            return BinaryOp(
                "+",
                BinaryOp("*", diff_ast(a, var), b),
                BinaryOp("*", a, diff_ast(b, var)),
            )
        case BinaryOp("/", a, b):
            # (a/b)' = (a'*b - a*b') / b^2
            numerator = BinaryOp(
                "-",
                BinaryOp("*", diff_ast(a, var), b),
                BinaryOp("*", a, diff_ast(b, var)),
            )
            denominator = BinaryOp("^", b, Number(2))
            return BinaryOp("/", numerator, denominator)
        case BinaryOp("^", a, Number(n)):
            # (a^n)' = n * a^(n-1) * a'
            return BinaryOp(
                "*",
                BinaryOp("*", Number(n), BinaryOp("^", a, Number(n - 1))),
                diff_ast(a, var),
            )
        case _:
            raise NotImplementedError(f"No rule for node: {node}")
