"""
This module contains utility functions and classes
that implement the pipe (|) functionality.
"""


from abc import abstractmethod
from typing import Any, Callable, Iterable, Hashable
from typing_extensions import Self


class BaseWrapper:
    """
    A base class for wrapper classes that implement the pipe (|) functionality.

    This class should not be instantiated directly, but rather be subclassed
    by other wrapper classes.
    """

    def __init__(self: Self, func: Callable[[Any], Any]):
        self.func = func

    def __call__(
        self: Self,
        *args: tuple[Any],
        **kwargs: dict[Hashable, Any],
    ) -> Any:
        return self.func(*args, **kwargs)

    def __repr__(self: Self) -> str:
        return f'{self.__class__.__name__}(func={self.func.__name__})'

    @abstractmethod
    def __ror__(self: Self, other: Iterable[Any]) -> Any:
        ...


class PipedWrapper(BaseWrapper):
    """
    A wrapper class for functions that
    can be used with the pipe (|) operator.

    Attributes:
        func (callable): The wrapped function.
    """

    # pylint: disable=too-few-public-methods

    def __ror__(self: Self, other: Iterable[Any]) -> Any:
        for item in other:
            yield self.func(item)


class FilteredWrapper(BaseWrapper):
    """
    A wrapper class for filter functions that
    can be used with the pipe (|) operator.

    Attributes:
        func (callable): The wrapped filter function.
    """

    # pylint: disable=too-few-public-methods

    def __ror__(self, other: Iterable[Any]) -> Any:
        for item in other:
            if self.func(item):
                yield item


class Collector:
    """
    A class representing the collector in the pipe (|) operator chain.

    This class collects the results of piped
    operations and returns them as a list.
    """

    # pylint: disable=too-few-public-methods

    def __repr__(self: Self) -> str:
        return 'Collector()'

    def __ror__(self: Self, other: Iterable[Any]) -> list[Any]:
        return list(other)


class Taker:
    """
    A class that takes a specified number of items from an input iterable.

    Attributes:
        number_of_items (int): The number of items to
        take from the input iterable.
    """

    def __init__(self: Self, number_of_items: int):
        self.number_of_items = number_of_items

    def __repr__(self: Self) -> str:
        return f'Taker(number_of_items={self.number_of_items})'

    def __ror__(self: Self, iterable: Iterable[Any]) -> Iterable[Any]:
        for i, item in enumerate(iterable):
            if i >= self.number_of_items:
                break
            yield item


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


def collect() -> Collector:
    """
    A function that creates and returns a Collector instance.

    Returns:
        Collector: A new Collector instance.
    """

    return Collector()


def take(number_of_items: int) -> Taker:
    """
    A function that creates and returns a Taker instance.

    Args:
        number_of_items (int): The number of items to take from
        the input iterable.

    Returns:
        Taker: A new Taker instance.
    """

    return Taker(number_of_items)
