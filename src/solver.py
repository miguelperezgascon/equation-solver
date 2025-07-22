from typing import Tuple, List, Dict, Optional, Union
import math


def solve_linear(a: float, b: float) -> Tuple[float]:
    if a == 0:
        raise ValueError("Coefficient 'a' must be non-zero for a linear equation.")
    return (-b / a,)


def solve_quadratic(a: float, b: float, c: float) -> Tuple[complex, complex]:
    if a == 0:
        raise ValueError("Coefficient 'a' must not be zero.")
    discriminant = b * b - 4 * a * c
    if discriminant >= 0:
        root_disc = math.sqrt(discriminant)
    else:
        root_disc = complex(0, math.sqrt(-discriminant))
    root1 = (-b + root_disc) / (2 * a)
    root2 = (-b - root_disc) / (2 * a)
    return (root1, root2)


def evaluate_rpn(
    tokens: List[str], variable_values: Optional[Dict[str, float]] = None
) -> Union[float, complex]:
    stack: List[complex] = []
    variables: Dict[str, float] = variable_values if variable_values is not None else {}

    for token in tokens:
        # operator
        if token in ("+", "-", "*", "/", "^"):
            y = stack.pop()
            x = stack.pop()
            if token == "+":
                stack.append(x + y)
            elif token == "-":
                stack.append(x - y)
            elif token == "*":
                stack.append(x * y)
            elif token == "/":
                stack.append(x / y)
            elif token == "^":
                stack.append(x**y)
        # operand
        else:
            try:
                value = float(token)
            except ValueError:
                if token in variables:
                    value = variables[token]
                else:
                    raise ValueError(f"Unknown variable '{token}'")
            stack.append(value)

    if len(stack) != 1:
        raise ValueError("Stack has extra elements.")
    # Return as float if no imaginary part, else complex
    result = stack[0]
    if isinstance(result, complex) and result.imag != 0:
        return result
    return result.real
