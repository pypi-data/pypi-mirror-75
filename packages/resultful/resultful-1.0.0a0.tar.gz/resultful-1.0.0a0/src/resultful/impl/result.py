__all__ = ["Success", "Failure"]

from typing import Any, TypeVar, Generic, Literal, Final

import resultful

ValueType = TypeVar("ValueType")
ErrorType = TypeVar("ErrorType")


class Success(Generic[ValueType]):

    __slots__ = ("value",)

    def __init__(self, value: ValueType) -> None:
        self.value: Final[ValueType] = value

    def __repr__(self) -> str:
        return f"{resultful.__name__}.{type(self).__name__}({self.value!r})"

    # noinspection PyTypeChecker
    def __bool__(self) -> Literal[True]:
        return True

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.value == other.value


class Failure(Generic[ErrorType]):

    __slots__ = ("error",)

    def __init__(self, error: ErrorType) -> None:
        self.error: Final[ErrorType] = error

    def __repr__(self) -> str:
        return f"{resultful.__name__}.{type(self).__name__}({self.error!r})"

    # noinspection PyTypeChecker
    def __bool__(self) -> Literal[False]:
        return False

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.error == other.error
