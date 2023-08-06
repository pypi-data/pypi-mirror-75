"""Python JSON:API core link types."""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from uri import URI

from python_jsonapi.core.types import Mixable
from python_jsonapi.core.types import Mixin
from python_jsonapi.core.types.meta import MetaMixin


class Link(Mixable, MetaMixin):
    """Class to represent a JSON:API link object.

    Attributes:
        href (URI): The uri for the link
        rel (List[str], optional): The link relation. Defaults to None.
    """

    def __init__(
        self, *, href: URI, rel: Optional[List[str]] = None, **kwargs: Any
    ) -> None:
        """Initializes a link.

        Args:
            href: The uri for the link
            rel: The link relation. Defaults to None.
            kwargs: Extra kwargs to pass along.
        """
        self.href = href
        self.rel = rel
        super().__init__(**kwargs)


class LinksMixin(Mixin):
    """Mixin to add to all types that support a JSON:API links object.

    Attributes:
        links (Dict[str, Link], optional):
            The link object.
    """

    def __init__(
        self, *, links: Optional[Dict[str, Link]] = None, **kwargs: Any
    ) -> None:
        """Initializes the links mixin.

        Args:
            links: The links object. Defaults to None.
            kwargs: Extra kwargs to pass along.
        """
        self.links = links
        super().__init__(**kwargs)

    def add_link(self, *, key: str, link: Link) -> None:
        """Adds a new link to the links object.

        Args:
            key: They key to use in the links object dictionary.
            link: The link to add.
        """
        if not self.links:
            self.links = {}
        self.links[key] = link
