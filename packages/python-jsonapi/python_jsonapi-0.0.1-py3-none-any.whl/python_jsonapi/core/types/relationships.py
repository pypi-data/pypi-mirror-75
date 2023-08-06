"""Python JSON:API core relationship types."""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from python_jsonapi.core.types import Mixable
from python_jsonapi.core.types import Mixin
from python_jsonapi.core.types.links import LinksMixin
from python_jsonapi.core.types.meta import MetaMixin
from python_jsonapi.core.types.resource_identifier import ResourceIdentifier


class Relationship(Mixable, LinksMixin, MetaMixin):
    """Class to represent a JSON:API relationship object.

    Attributes:
        data (Union[ResourceIdentifier, List[ResourceIdentifier]], optional):
            The resource linkage. Defaults to None.
    """

    def __init__(
        self,
        *,
        data: Optional[Union[ResourceIdentifier, List[ResourceIdentifier]]] = None,
        **kwargs: Any
    ) -> None:
        """Initializes a relationship.

        Args:
            data: The resource linkage. Defaults to None.
            kwargs: Extra kwargs to pass along.
        """
        self.data = data
        super().__init__(**kwargs)


class RelationshipsMixin(Mixin):
    """Mixin to add to all types that support a JSON:API relationships object.

    Attributes:
        relationships (Dict[str, Relationship], optional):
            The relationships object. Defaults to None
    """

    def __init__(
        self, *, relationships: Optional[Dict[str, Relationship]] = None, **kwargs: Any
    ) -> None:
        """Initializes the relationships mixin.

        Args:
            relationships: The relationships object. Defaults to None.
            kwargs: Extra kwargs to pass along.
        """
        self.relationships = relationships
        super().__init__(**kwargs)

    def add_relationship(self, *, key: str, relationship: Relationship) -> None:
        """Adds a new relationship entry to the relationships object.

        Args:
            key: They key to use in the relationships object dictionary.
            relationship: The relationship entry to add.
        """
        if not self.relationships:
            self.relationships = {}
        self.relationships[key] = relationship
