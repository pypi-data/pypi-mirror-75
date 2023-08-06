from typing import Union, Optional
from .resulthandle import ResultHandle


class CircuitNotValidError(Exception):
    """Raised when a submitted circuit does not satisfy all predicates"""

    def __init__(self, message: Union[str, int], failed_pred: Optional[str] = None):
        if isinstance(message, int):
            message = (
                "Circuit with index {0} in submitted does not satisfy "
                "{1} (try running backend.compile_circuit(circuit) first)."
            ).format(message, failed_pred or "all predicates")
        super().__init__(message)


class CircuitNotRunError(Exception):
    """Raised when a result is retrieved corresponding to a handle that has not been executed"""

    def __init__(self, handle: ResultHandle):
        super().__init__(
            "Circuit corresponding to {0!r} has not been run by this backend instance.".format(
                handle
            )
        )


class InvalidResultType(Exception):
    """Raised when a BackendResult instance cannot produce the required result type."""

    def __init__(self, result_type: str):
        super().__init__(
            "BackendResult cannot produce result of type {}.".format(result_type)
        )
