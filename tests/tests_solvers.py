# tests/tests_solvers.py
import pytest
import cmath
from src.solvers import roots_companion, brent, durand_kerner, solve


# roots of x^2 - 1 = 0 are 1 and -1
def test_roots_companion():
    roots = roots_companion([-1, 0, 1])
    assert set(round(r.real) for r in roots) == {1, -1}


# Brent solves f(x)=x-2 in [0,4]
def test_brent():
    f = lambda x: x - 2
    root = brent(f, 0, 4)
    assert abs(root - 2) < 1e-8


# Durand-Kerner for x^2 - 1 = 0
def test_durand_kerner():
    roots = durand_kerner([-1, 0, 1])
    vals = set(round(r.real) for r in roots)
    assert vals == {1, -1}


# solve polynomial
def test_solve_polynomial():
    roots = solve("x^2 - 1 = 0")
    assert set(round(r.real) for r in roots) == {1, -1}


# solve generic real root
def test_solve_generic():
    roots = solve("sin(x) - 0 = 0", domain=(1, 4))
    # sin(x)=0 has root at pi ~3.1415
    assert abs(roots[0] - cmath.pi) < 1e-3
