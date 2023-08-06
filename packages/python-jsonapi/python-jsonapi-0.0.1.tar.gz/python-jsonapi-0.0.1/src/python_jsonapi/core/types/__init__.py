"""Python JSON:API core type classes."""
from typing import Any


class Mixable:
    """Base class for all classes that support mixins.

    Mixables need to use named arguments for all of their arguments.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initializes the mixable."""
        super().__init__(**kwargs)  # type: ignore # mypy issue 433


class Mixin:
    """Base class for all classes that are mixins.

    Mixins need to use named arguments for all of their arguments.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initializes the mixin."""
        super().__init__(**kwargs)  # type: ignore # mypy issue 433
