# evaluator.py
from src.ast import AST, Number, Variable, UnaryOp, BinaryOp
import cmath


def eval_ast(node: AST, env: dict[str, complex], var: str = "x") -> complex:
    match node:
        case Number(v):
            return v
        case Variable(n):
            return env.get(n, 0)
        case UnaryOp("neg", u):
            return -eval_ast(u, env, var)
        case UnaryOp("sin", u):
            return cmath.sin(eval_ast(u, env, var))
        case UnaryOp("cos", u):
            return cmath.cos(eval_ast(u, env, var))
        case UnaryOp("tan", u):
            return cmath.tan(eval_ast(u, env, var))
        case BinaryOp("+", a, b):
            return eval_ast(a, env, var) + eval_ast(b, env, var)
        case BinaryOp("-", a, b):
            return eval_ast(a, env, var) - eval_ast(b, env, var)
        case BinaryOp("*", a, b):
            return eval_ast(a, env, var) * eval_ast(b, env, var)
        case BinaryOp("/", a, b):
            return eval_ast(a, env, var) / eval_ast(b, env, var)
        case BinaryOp("^", a, b):
            return eval_ast(a, env, var) ** eval_ast(b, env, var)
        case _:
            raise ValueError(f"Unkown AST node: {node}")
