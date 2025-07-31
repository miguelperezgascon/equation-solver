# main.py
import argparse
from src.solvers import solve


def main():
    parser = argparse.ArgumentParser(
        description="Solve equations of the form f(x)=0 (polynomial or generic)."
    )
    parser.add_argument(
        "expr",
        type=str,
        help='Equation in infix form, e.g. "x^2 - 1 = 0" or "sin(x) - 0 = 0"',
    )
    parser.add_argument(
        "--domain",
        nargs=2,
        type=float,
        metavar=("A", "B"),
        help="Optional real interval [A, B] to search for roots",
    )
    args = parser.parse_args()

    domain = tuple(args.domain) if args.domain else None
    roots = solve(args.expr, domain=domain)

    if not roots:
        print("No roots found.")
    else:
        print("Roots found:")
        for r in roots:
            # Pretty-print real vs. complex
            if abs(r.imag) < 1e-8:
                print(f"  {r.real:.8g}")
            else:
                print(f"  {r.real:.8g} + {r.imag:.8g}j")


if __name__ == "__main__":
    main()
