__all__ = [
    "Result",
    "ResultType",
    "NoResultType",
    "success",
    "failure",
    "unwrap_success",
    "unwrap_failure",
    "NoResult",
]

# Annotations

from .ui import Result

# Types

from .ui import (
    ResultType,
    NoResultType,
)

# Concretes

from .ui import (
    success,
    failure,
    unwrap_success,
    unwrap_failure,
    NoResult,
)
