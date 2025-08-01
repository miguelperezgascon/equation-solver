# Equation Solver

Advanced symbolic and numerical solver for mathematical equations — now supporting **functions**, **symbolic differentiation**, and **nonlinear solving**.

## Features

- ✅ Tokenization and parsing using the **Shunting‑Yard algorithm**
- ✅ Full **AST (Abstract Syntax Tree)** representation
- ✅ Unary functions: `sin`, `cos`, `tan`, `neg`
- ✅ Expression evaluation (including complex numbers)
- ✅ Symbolic differentiation (`d/dx`)
- ✅ Equation solving via:
  - Polynomial methods (Companion matrix, Durand-Kerner)
  - Brent's method for generic expressions over real intervals
- ✅ Real and complex root support
- ✅ Fully tested with `pytest`

---

## Installation

Clone the repository:

```bash
git clone git@github.com:miguelperezgascon/equation-solver.git
cd equation-solver
```

Install dependencies (if needed):

```bash
pip install -r requirements.txt
```

> Note: The project works with standard Python libraries only.

---

## Run Tests

```bash
pytest
```

---

## Usage

Run from the command line:

```bash
python main.py "x^2 - 4 = 0"
```

### ✨ Examples

```bash
# Quadratic
$ python main.py "x^2 - 4 = 0"
Roots: [-2.0, 2.0]

# Linear
$ python main.py "2*x + 5 = 0"
Root: [-2.5]

# Transcendental
$ python main.py "sin(x) - 0 = 0" --domain 1 4
Root in domain: [3.1416]
```

---

## Project Structure

- `src/parser.py` — Tokenizer, Shunting-Yard algorithm, RPN, AST builder
- `src/evaluator.py` — Expression evaluator
- `src/differentiator.py` — Symbolic differentiation engine
- `src/solvers.py` — Equation solvers (exact & numerical)
- `tests/` — Test suite for parser, evaluator, solver, differentiator

---

## Roadmap

- ⏳ Test problems to be sorted out
