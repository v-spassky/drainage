"""
This module contains utility functions and classes
that implement the pipe (|) functionality.
"""


from typing import Any, Callable, Iterable, Hashable
from typing_extensions import Self


class PipedWrapper:
    """
    A wrapper class for functions that
    can be used with the pipe (|) operator.

    Attributes:
        func (callable): The wrapped function.
    """

    def __init__(self, func: Callable[[Any], Any]):
        self.func = func

    def __call__(
        self: Self,
        *args: tuple[Any],
        **kwargs: dict[Hashable, Any],
    ) -> Any:
        return self.func(*args, **kwargs)

    def __ror__(self: Self, other: Iterable[Any]) -> Any:
        for item in other:
            yield self.func(item)


class FilteredWrapper:
    """
    A wrapper class for filter functions that
    can be used with the pipe (|) operator.

    Attributes:
        func (callable): The wrapped filter function.
    """

    def __init__(self: Self, func: Callable[[Any], Any]):
        self.func = func

    def __call__(
        self: Self,
        *args: tuple[Any],
        **kwargs: dict[Hashable, Any],
    ) -> Any:
        return self.func(*args, **kwargs)

    def __ror__(self, other: Iterable[Any]) -> Any:
        for item in other:
            if self.func(item):
                yield item


class PipedCollector:
    """
    A class representing the collector in the pipe (|) operator chain.

    This class collects the results of piped
    operations and returns them as a list.
    """

    # pylint: disable=too-few-public-methods

    def __ror__(self: Self, other: Iterable[Any]) -> list[Any]:
        return list(other)


def piped(func: Callable[[Any], Any]) -> PipedWrapper:
    """
    A decorator that wraps a function with the PipedWrapper class.

    Args:
        func (Callable[[Any], Any]): The function to be wrapped.

    Returns:
        PipedWrapper: The wrapped function.
    """

    return PipedWrapper(func)


def filtered(func: Callable[[Any], Any]) -> FilteredWrapper:
    """
    A decorator that wraps a filter function with the FilteredWrapper class.

    Args:
        func (Callable[[Any], Any]): The filter function to be wrapped.

    Returns:
        FilteredWrapper: The wrapped filter function.
    """

    return FilteredWrapper(func)


def collect() -> PipedCollector:
    """
    A function that creates and returns a PipedCollector instance.

    Returns:
        PipedCollector: A new PipedCollector instance.
    """

    return PipedCollector()
