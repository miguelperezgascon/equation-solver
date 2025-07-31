# solvers.py
from typing import List, Tuple, Optional, Dict
import numpy as np
import cmath
from src.ast import AST, Number, Variable, UnaryOp, BinaryOp
from src.evaluator import eval_ast
from src.differentiator import diff_ast


def roots_companion(coeffs: List[complex]) -> List[complex]:
    if coeffs[-1] == 0:
        raise ValueError("Leading coefficient must not be zero")
    # Normalize to monic: x^n + b_{n-1} x^{n-1} + ... + b0
    b = [-c / coeffs[-1] for c in coeffs[:-1]]
    n = len(b)
    # Construct cmpanion matrix
    C = np.zeros((n, n), dtype=complex)
    C[:-1, 1:] = np.eye(n - 1)
    C[-1, :] = b[::-1]
    # Compute eigenvalues
    roots = np.linalg.eigvals(C)
    return roots.tolist()


def brent(f, a: float, b: float, tol: float = 1e-8, maxiter: int = 100) -> float:
    fa, fb = f(a), f(b)
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) and f(b) must have different signs")
    if abs(fa) < abs(fb):
        a, b, fa, fb = b, a, fb, fa
    c, fc, d, e = a, fa, b - a, b - a
    for _ in range(maxiter):
        if fb == 0 or abs(b - a) < tol:
            return b

        if fa != fc and fb != fc:
            # Inverse Quadratic Interpolation (IQI)
            denom_af = (fa - fb) * (fa - fc)
            denom_bf = (fb - fa) * (fb - fc)
            denom_cf = (fc - fa) * (fc - fb)
            s = a * fb * fc / denom_af + b * fa * fc / denom_bf + c * fa * fb / denom_cf
        else:
            # Secant method
            s = b - fb * (b - a) / (fb - fa)

        cond_bisect = (
            not ((3 * a + b) / 4 < s < b)
            or abs(e) < tol
            or abs(s - b) >= abs(b - c) / 2
        )
        if cond_bisect:
            # Bisection step
            s = (a + b) / 2
            e = d = b - a
        else:
            e, d = d, b - s

        fs = f(s)
        c, fc = b, fb

        if fa * fs < 0:
            b, fb = s, fs
        else:
            a, fa = s, fs

        if abs(fa) < abs(fb):
            a, b = b, a
            fa, fb = fb, fa
    return b


def durand_kerner(
    coeffs: List[complex], tol: float = 1e-8, maxiter: int = 100
) -> List[complex]:
    n = len(coeffs) - 1
    # Initial guesses: roots of unity scaled
    roots = [cmath.exp(2j * cmath.pi * i / n) for i in range(n)]
    for _ in range(maxiter):
        new_roots = []
        for i in range(n):
            prod = 1
            for j in range(n):
                if i != j:
                    prod *= roots[i] - roots[j]
            # Evaluate poly at roots[i]
            p = sum(coeffs[k] * roots[i] ** k for k in range(n + 1))
            new_roots.append(roots[i] - p / prod)
        if all(abs(new_roots[i] - roots[i]) < tol for i in range(n)):
            break
        roots = new_roots
    return roots


def _extract_coeffs(ast: AST, var: str = "x") -> Dict[int, complex]:
    """
    Recursively extract polynomial coefficients from AST as a map power->coeff.
    """
    if isinstance(ast, Number):
        return {0: ast.value}
    if isinstance(ast, Variable) and ast.name == var:
        return {1: 1}
    if isinstance(ast, BinaryOp):
        if ast.op == "+":
            c1 = _extract_coeffs(ast.left, var)
            c2 = _extract_coeffs(ast.right, var)
            for p, c in c2.items():
                c1[p] = c1.get(p, 0) + c
            return c1
        if ast.op == "-":
            c1 = _extract_coeffs(ast.left, var)
            c2 = _extract_coeffs(ast.right, var)
            for p, c in c2.items():
                c1[p] = c1.get(p, 0) - c
            return c1
        if ast.op == "*":
            c1 = _extract_coeffs(ast.left, var)
            c2 = _extract_coeffs(ast.right, var)
            res: Dict[int, complex] = {}
            for p1, c1v in c1.items():
                for p2, c2v in c2.items():
                    res[p1 + p2] = res.get(p1 + p2, 0) + c1v * c2v
            return res
        if ast.op == "^" and isinstance(ast.right, Number):
            exp = int(ast.right.value.real)
            base = ast.left
            res = {0: 1}
            for _ in range(exp):
                res = {
                    p1 + p2: c1 * c2
                    for p1, c1 in res.items()
                    for p2, c2 in _extract_coeffs(base, var).items()
                }
            return res
    raise ValueError("Non-polynomial AST node encountered")


def solve(
    expr: str,
    domain: Optional[Tuple[float, float]] = None,
    tol: float = 1e-8,
    max_subintervals: int = 100,
) -> List[complex]:
    from src.parser import parse

    lhs, rhs = parse(expr)

    # Polynomial branch
    if domain is None:
        # Extract coefficients for polynomial a0 + a1 x + ...
        coeffs_map = _extract_coeffs(BinaryOp("-", lhs, rhs))
        max_pow = max(coeffs_map)
        coeffs = [coeffs_map.get(i, 0) for i in range(max_pow + 1)]
        return roots_companion(coeffs)

    # generic real root finding
    def f(x: complex) -> complex:
        return eval_ast(lhs, {"x": x}, "x") - eval_ast(rhs, {"x": x}, "x")

    a, b = domain
    xs = np.linspace(a, b, max_subintervals + 1)
    roots: List[complex] = []
    for i in range(len(xs) - 1):
        x0, x1 = xs[i], xs[i + 1]
        try:
            if f(x0).real * f(x1).real < 0:
                root = brent(lambda t: f(t).real, x0, x1, tol)
                roots.append(root)
        except ValueError:
            continue
    # Remove duplicates within tolerance
    unique_roots: List[complex] = []
    for r in roots:
        if not any(abs(r - u) < tol for u in unique_roots):
            unique_roots.append(r)
    return unique_roots
