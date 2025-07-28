# solvers.py
from typing import List, Tuple, Optional
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
