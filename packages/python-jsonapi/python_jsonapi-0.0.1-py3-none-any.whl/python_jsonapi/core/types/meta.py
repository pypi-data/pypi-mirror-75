"""Python JSON:API core meta types."""
from typing import Any
from typing import Dict
from typing import Optional

from python_jsonapi.core.types import Mixin


class Meta:
    """Class to represent a JSON:API meta object entry."""

    pass


class MetaMixin(Mixin):
    """Mixin to add to all types that support a JSON:API meta object.

    Attributes:
        meta (Dict[str, Meta], optional):
            The meta object.
    """

    def __init__(
        self, *, meta: Optional[Dict[str, Meta]] = None, **kwargs: Any
    ) -> None:
        """Initializes the meta mixin.

        Args:
            meta: The meta object. Defaults to None.
            kwargs: Extra kwargs to pass along.
        """
        self.meta = meta
        super().__init__(**kwargs)

    def add_meta(self, *, key: str, meta: Meta) -> None:
        """Adds a new meta entry to the meta object.

        Args:
            key: The key for the dictionary.
            meta: The meta entry to add.
        """
        if not self.meta:
            self.meta = {}
        self.meta[key] = meta
