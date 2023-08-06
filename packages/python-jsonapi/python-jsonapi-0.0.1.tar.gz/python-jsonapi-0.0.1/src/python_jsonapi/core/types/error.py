"""Python JSON:API core error types."""
from typing import Any
from typing import Optional

from python_jsonapi.core.types import Mixable
from python_jsonapi.core.types.links import LinksMixin
from python_jsonapi.core.types.meta import MetaMixin


class ErrorSource:
    """Class to represent a JSON:API error source object.

    Attributes:
        pointer (str, optional):
            A JSON Pointer [RFC6901] to the associated entity in the request document.
        parameter (str, optional):
            A string indicating which URI query parameter caused the error.
    """

    def __init__(
        self, *, pointer: Optional[str] = None, parameter: Optional[str] = None
    ) -> None:
        """Initializes an error source object.

        Args:
            pointer: A JSON Pointer [RFC6901] to the associated entity in the request document.
            parameter: A string indicating which URI query parameter caused the error.
        """
        self.pointer = pointer
        self.parameter = parameter


class Error(Mixable, LinksMixin, MetaMixin):
    """Class to represent a JSON:API error object.

    Attributes:
        id (str):
            A unique identifier for the particular occurrence of the error.
        status (str):
            The HTTP status code applicable to this problem, expressed as a
            string value.
        code (str):
            An application-specific error code, expressed as a string value.
        title (str):
            A short, human-readable summary of the problem that SHOULD NOT
            change from occurrence to occurrence of the problem, except for
            purposes of localization.
        detail (str):
            A human-readable explanation specific to this occurrence of the
            problem. Like title, this field’s value can be localized.
        source (ErrorSource):
            An object containing references to the source of the error
    """

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        status: Optional[str] = None,
        code: Optional[str] = None,
        title: Optional[str] = None,
        detail: Optional[str] = None,
        source: Optional[ErrorSource] = None,
        **kwargs: Any
    ) -> None:
        """Initializes an error object.

        Args:
            id: A unique identifier for the error. Defaults to None.
            status: The HTTP status code. Defaults to None.
            code: An application-specific error code. Defaults to None.
            title: A short, human-readable summary of the problem. Defaults to None.
            detail: A human-readable explanation specific to problem. Defaults to None.
            source: References to the source of the error. Defaults to None.
            kwargs: Extra kwargs to pass along.
        """
        self.id = id
        self.status = status
        self.code = code
        self.title = title
        self.detail = detail
        self.source = source
        super().__init__(**kwargs)
