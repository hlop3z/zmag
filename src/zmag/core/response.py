from dataclasses import dataclass


@dataclass
class Error:
    """A single error inside a `Result.errors` list."""

    code: str
    message: str
    field: str | None = None
