# src/main.py
import sys
import re
from typing import Tuple
from parser import tokenize, to_rpn
from solver import solve_linear, solve_quadratic, evaluate_rpn


def extract_coeffs(expr: str) -> Tuple[float, float, float]:
    """
    Extract coefficients a, b, c from a polynomial expression up to degree 2.
    Supports expressions of form: ax^2 + bx + c.
    """
    s = expr.replace(" ", "")
    pat_a = re.compile(r"([+-]?\d*\.?\d*)\*?x\^2")
    pat_b = re.compile(r"([+-]?\d*\.?\d*)\*?x(?!\^)")
    pat_c = re.compile(r"([+-]?\d+\.?\d*)(?![x\d*])$")

    def parse(pat: re.Pattern) -> float:
        m = pat.search(s)
        if not m:
            return 0.0
        v = m.group(1)
        if v in ("", "+"):
            return 1.0
        if v == "-":
            return -1.0
        return float(v)

    return (parse(pat_a), parse(pat_b), parse(pat_c))


def main():
    # Read expression from args or input
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
    else:
        expr = input("Enter equation (e.g. 2*x^2 + 3*x + 4 = 0): ")

    # Split LHS/RHS
    if "=" in expr:
        lhs, rhs = expr.split("=", 1)
    else:
        lhs, rhs = expr, "0"
    lhs = lhs.strip()
    rhs = rhs.strip()

    # Normalize: if RHS is zero, use LHS directly; else subtract RHS
    if rhs == "0":
        norm = lhs
    else:
        norm = f"({lhs})-({rhs})"

    try:
        a, b, c = extract_coeffs(norm)
        if a != 0.0:
            r1, r2 = solve_quadratic(a, b, c)
            print(f"Quadratic roots: {r1}, {r2}")
        elif b != 0.0:
            (r,) = solve_linear(b, c)
            print(f"Linear root: {r}")
        else:
            print("No variable term: constant equation.")
    except Exception as e:
        # Fallback: generic RPN evaluation at x=1
        print(f"Extraction failed ({e}), evaluating at x=1")
        tokens = tokenize(norm)
        rpn = to_rpn(tokens)
        result = evaluate_rpn(rpn, variable_values={"x": 1.0})
        print(f"Result: {result}")


if __name__ == "__main__":
    main()
