"""
This module contains test suite for the `drainage` package.
"""


from drainage import collect, filtered, piped, reduced, sliced, take


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


def test_sliced_function():
    """
    Ensures that the `sliced()` function works correctly in pipe expressions.
    """

    first_three_evens = (
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        | is_even
        | sliced[:3]
        | collect()
     )
    assert first_three_evens == [2, 4, 6]

    first_two_longer_than_five = (
        ["apple", "banana", "cherry", "avocado", "grape"]
        | has_length_greater_than_five
        | sliced[:2]
        | collect()
    )
    assert first_two_longer_than_five == ["banana", "cherry"]


def test_reduced_function():
    """
    Ensures that the `reduced()` function works correctly in pipe expressions.
    """

    sum_of_evens = (
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        | is_even
        | reduced(lambda acc, num: acc + num)
    )
    assert sum_of_evens == 30

    sum_of_squares = (
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        | square
        | reduced(lambda acc, num: acc + num)
    )
    assert sum_of_squares == 385

    sum_of_lengths = (
        ["apple", "banana", "cherry", "avocado", "grape"]
        | reduced(lambda acc, word: acc + len(word))
    )
    assert sum_of_lengths == len("apple" "banana" "cherry" "avocado" "grape")

    product_of_evens = (
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        | is_even
        | reduced(lambda acc, num: acc * num, acc=1) # notice the `acc`
    )
    assert product_of_evens == 2 * 4 * 6 * 8 * 10

    product_of_squares = (
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        | square
        | reduced(lambda acc, num: acc * num, acc=1) # notice the `acc`
    )
    assert product_of_squares == 1 * 4 * 9 * 16 * 25 * 36 * 49 * 64 * 81 * 100


def test_collect_function():
    """
    Ensures that the `collect()` function works correctly in pipe expressions.
    """

    evens = (
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        | is_even
        | collect()
     )
    assert evens == [2, 4, 6, 8, 10]

    squares = (
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        | square
        | collect()
     )
    assert squares == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

    squares_tuple = (
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        | square
        | collect(constructor=tuple)
    )
    assert squares_tuple == (1, 4, 9, 16, 25, 36, 49, 64, 81, 100)

    unique_words_starting_with_a = (
        ["apple", "banana", "cherry", "banana", "avocado", "grape", "apple"]
        | starts_with_a
        | collect(constructor=set)
     )
    assert unique_words_starting_with_a == {"apple", "avocado"}


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


def test_string_representation_of_wrappers():
    """
    Ensures that the string representation of wrapper classes is correct.
    """

    assert str(add_one) == 'PipedWrapper(func=add_one)'
    assert repr(add_one) == 'PipedWrapper(func=add_one)'
    assert format(add_one) == 'PipedWrapper(func=add_one)'

    assert str(is_even) == 'FilteredWrapper(func=is_even)'
    assert repr(is_even) == 'FilteredWrapper(func=is_even)'
    assert format(is_even) == 'FilteredWrapper(func=is_even)'

    assert str(sliced[:3]) == 'Slicer(start=0, stop=3, step=1)'
    assert repr(sliced[:3]) == 'Slicer(start=0, stop=3, step=1)'
    assert format(sliced[:3]) == 'Slicer(start=0, stop=3, step=1)'

    reducer_str = str(reduced(lambda acc, next: acc + next))
    assert reducer_str == 'Reducer(func=<lambda>, acc=0)'
    reducer_repr = repr(reduced(lambda acc, next: acc + next))
    assert reducer_repr == 'Reducer(func=<lambda>, acc=0)'
    reducer_format = format(reduced(lambda acc, next: acc + next))
    assert reducer_format == 'Reducer(func=<lambda>, acc=0)'

    assert str(collect()) == 'Collector(constructor=list)'
    assert repr(collect()) == 'Collector(constructor=list)'
    assert format(collect()) == 'Collector(constructor=list)'

    assert str(take(3)) == 'Taker(number_of_items=3)'
    assert repr(take(3)) == 'Taker(number_of_items=3)'
    assert format(take(3)) == 'Taker(number_of_items=3)'
