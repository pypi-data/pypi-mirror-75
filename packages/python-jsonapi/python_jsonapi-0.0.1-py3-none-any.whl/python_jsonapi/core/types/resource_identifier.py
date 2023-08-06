"""Python JSON:API core resource identifier types."""
from typing import Any

from python_jsonapi.core.types import Mixable
from python_jsonapi.core.types import Mixin
from python_jsonapi.core.types.meta import MetaMixin


class ResourceIdentifiableMixin(Mixin):
    """A mixin for resource identifiable objects.

    Attributes:
        type (str):
            The type of the resource.
        id (str):
            The id of the resource.
    """

    def __init__(self, *, type: str, id: str, **kwargs: Any) -> None:
        """Initializes the resource identifiable mixin.

        Args:
            type: The type of the resource.
            id: The id of the resource.
            kwargs: Extra kwargs to pass along.
        """
        self.type = type
        self.id = id
        super().__init__(**kwargs)


class ResourceIdentifier(Mixable, ResourceIdentifiableMixin, MetaMixin):
    """A class for a JSON:API resource identifier object."""

    def __init__(self, **kwargs: Any) -> None:
        """Initializes the resource identifer object.

        Args:
            kwargs: Extra kwargs to pass along.
        """
        super().__init__(**kwargs)
