# utils.py
from typing import Callable, TypeVar, Generic, Optional, Union, Any, cast

T = TypeVar("T")
U = TypeVar("U")


def compose(f: Callable[[U], T], g: Callable[..., U]) -> Callable[..., T]:
    """
    Compose two functions f ∘ g.
    Returns a function h(*args) = f(g(*args)).
    """
    return lambda *args, **kwargs: f(g(*args, **kwargs))


class Maybe(Generic[T]):
    """
    Maybe monad for optional values without exceptions.
    """

    def __init__(self, value: Optional[T]):
        self._value: Optional[T] = value

    def is_some(self) -> bool:
        return self._value is not None

    def map(self, fn: Callable[[T], U]) -> "Maybe[U]":
        if self.is_some():
            # type narrowing: _value is T
            val = cast(T, self._value)
            return Maybe(fn(val))
        return Maybe(None)

    def unwrap_or(self, default: U) -> Union[T, U]:
        return cast(T, self._value) if self.is_some() else default


class Either(Generic[T, U]):
    """
    Either monad for functional error handling.
    Left: error value; Right: success.
    """

    def __init__(self, left: Optional[T] = None, right: Optional[U] = None):
        self.left: Optional[T] = left
        self.right: Optional[U] = right

    def is_right(self) -> bool:
        return self.right is not None

    def map(self, fn: Callable[[U], Any]) -> "Either[T, Any]":
        if self.is_right():
            val = cast(U, self.right)
            return Either(right=fn(val))
        return Either(left=self.left)
