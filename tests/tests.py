"""
This module contains test suite for the `drainage` package.
"""


from drainage import collect, filtered, piped, take


@piped
def add_one(x):
    return x + 1


@piped
def multiply_by_two(x):
    return x * 2


@piped
def square(x):
    return x ** 2


@piped
def fizzbuzz(x):
    if x % 15 == 0:
        return "FizzBuzz"
    elif x % 3 == 0:
        return "Fizz"
    elif x % 5 == 0:
        return "Buzz"
    else:
        return x


@piped
def add_prefix_hello(x):
    return f"Hello {x}"


@piped
def reverse_string(x):
    return x[::-1]


@filtered
def is_even(x):
    return x % 2 == 0


@filtered
def is_odd(x):
    return x % 2 != 0


@filtered
def is_positive(x):
    return x > 0


@filtered
def has_length_greater_than_five(x):
    return len(x) > 5


@filtered
def starts_with_a(x):
    return x.lower().startswith("a")


def test_piped_decorated_functions_work_the_same():
    """
    Ensures that applying the `@piped` decorator to
    a function does not change its default behavior.
    """

    assert add_one(1) == 2
    assert add_one(2) == 3
    assert add_one(3) == 4

    assert multiply_by_two(2) == 4
    assert multiply_by_two(3) == 6
    assert multiply_by_two(4) == 8

    assert square(2) == 4
    assert square(3) == 9
    assert square(4) == 16

    assert fizzbuzz(1) == 1
    assert fizzbuzz(2) == 2
    assert fizzbuzz(3) == "Fizz"
    assert fizzbuzz(4) == 4
    assert fizzbuzz(5) == "Buzz"
    assert fizzbuzz(6) == "Fizz"
    assert fizzbuzz(7) == 7
    assert fizzbuzz(15) == "FizzBuzz"

    assert add_prefix_hello("World") == "Hello World"
    assert add_prefix_hello("John") == "Hello John"

    assert reverse_string("Hello") == "olleH"
    assert reverse_string("World") == "dlroW"


def test_filtered_decorated_functions_work_the_same():
    """
    Ensures that applying the `@filtered` decorator to
    a function does not change its default behavior.
    """

    assert is_even(1) is False
    assert is_even(2) is True
    assert is_even(3) is False
    assert is_even(4) is True

    assert is_odd(1) is True
    assert is_odd(2) is False
    assert is_odd(3) is True
    assert is_odd(4) is False

    assert is_positive(1) is True
    assert is_positive(-1) is False
    assert is_positive(0) is False

    assert has_length_greater_than_five("apple") is False
    assert has_length_greater_than_five("banana") is True
    assert has_length_greater_than_five("orange") is True

    assert starts_with_a("apple") is True
    assert starts_with_a("banana") is False
    assert starts_with_a("orange") is False


def test_piped_decorator():
    """
    Ensures that functions decorated with `@piped`
    can be used in pipe expressions.
    """

    assert [1, 3, 4] | add_one | add_one | collect() == [3, 5, 6]
    assert [1, 2, 3] | multiply_by_two | collect() == [2, 4, 6]
    assert [1, 2, 3] | square | collect() == [1, 4, 9]

    greets = ["John", "Jane", "Doe"] | add_prefix_hello | collect()
    assert greets == ["Hello John", "Hello Jane", "Hello Doe"]

    reversed_words = ["Hello", "World"] | reverse_string | collect()
    assert reversed_words == ["olleH", "dlroW"]


def test_filtered_decorator():
    """
    Ensures that functions decorated with `@filtered`
    can be used in pipe expressions.
    """

    assert [1, 2, 3, 4] | is_even | collect() == [2, 4]
    assert [1, 2, 3, 4] | is_odd | collect() == [1, 3]
    assert [1, -2, 3, -4] | is_positive | collect() == [1, 3]

    longer_than_five = (
        ["apple", "banana", "cherry", "avocado"]
        | has_length_greater_than_five
        | collect()
    )
    assert longer_than_five  == ["banana", "cherry", "avocado"]

    starts_with_a_letter = (
        ["apple", "banana", "cherry", "avocado"]
        | starts_with_a
        | collect()
    )
    assert starts_with_a_letter == ["apple", "avocado"]


def test_take_function():
    """
    Ensures that the `take()` function works correctly in pipe expressions.
    """

    first_three_evens = (
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        | is_even
        | take(3)
        | collect()
     )
    assert first_three_evens == [2, 4, 6]

    first_four_squares = (
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        | square
        | take(4)
        | collect()
     )
    assert first_four_squares == [1, 4, 9, 16]

    first_with_a = (
        ["apple", "banana", "cherry", "avocado", "grape", "orange"]
        | starts_with_a
        | take(1)
        | collect()
    )
    assert first_with_a == ["apple"]

    first_two_gt_5 = (
        ["apple", "banana", "cherry", "avocado", "grape", "orange"]
        | has_length_greater_than_five
        | take(2)
        | collect()
    )
    assert first_two_gt_5 == ["banana", "cherry"]
