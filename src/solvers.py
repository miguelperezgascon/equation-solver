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
