# equation-solver
## Calculator for Polynomial Equations
- Currently working for polynomial equations up to degree 2.
- Infix parsing using a lexer.
- Shunting‑Yard algorithm.
- Reverse Polish Notation (RPN) evaluation.
- Supporting real and complex results.
- Fallback evaluator for arbitrary expressions at x = 1.

## Installation
1. Clone the repository:
```
git clone git@github.com:miguelperezgascon/equation-solver.git
cd equation-solver
```

## Usage
```
# Solve a quadratic equation
python src/main.py "x^2 + 6x + 8 = 0"
# Output:
# Quadratic roots: -4.0, -2.0

# Solve a linear equation
python src/main.py "2*x + 5 = 0"
# Output:
# Linear root: -2.5
```

