# differentiatior.py
from src.ast import AST, Number, Variable, UnaryOp, BinaryOp


def diff_ast(node: AST, var: str = "x") -> AST:
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
            # (a^n)' = n * a^(n-1) [* a'] (chain rule)
            n_int = int(n.real)
            new_power = BinaryOp("^", a, Number(n_int - 1))
            coeff = Number(n_int)
            base_deriv = diff_ast(a, var)
            if isinstance(base_deriv, Number) and base_deriv.value == 1:
                # avoid product of 1
                return BinaryOp("*", coeff, new_power)
            # chain rule
            return BinaryOp("*", BinaryOp("*", coeff, new_power), base_deriv)
        case _:
            raise NotImplementedError(f"No rule for node: {node}")
