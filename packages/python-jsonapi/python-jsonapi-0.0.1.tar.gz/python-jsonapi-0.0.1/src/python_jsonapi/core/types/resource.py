"""Python JSON:API core resource types."""
from typing import Any
from typing import Optional
from typing import TypedDict

from python_jsonapi.core.types import Mixable
from python_jsonapi.core.types.links import LinksMixin
from python_jsonapi.core.types.meta import MetaMixin
from python_jsonapi.core.types.relationships import RelationshipsMixin
from python_jsonapi.core.types.resource_identifier import ResourceIdentifiableMixin


class Resource(
    Mixable, ResourceIdentifiableMixin, LinksMixin, RelationshipsMixin, MetaMixin
):
    """A class for a JSON:API resource object.

    Attributes:
        attributes (Attributes, optional):
            The attributes for the resource. Defaults to None.
    """

    class Attributes(TypedDict):
        """Class to represent a JSON:API resource attributes object entry."""

        pass

    def __init__(self, attributes: Optional[Attributes] = None, **kwargs: Any) -> None:
        """Initializes the resource identifer object.

        Args:
            attributes: The attributes for the resource. Defaults to None.
            kwargs: Extra kwargs to pass along.
        """
        self.attributes = attributes
        super().__init__(**kwargs)
