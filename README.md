# `drainage`

A Python library that provides an implementation of UNIX-like pipes for Python
functions. Chain your functions together using the pipe (`|`) operator and
make your code more functional and expressive.


### Installation

```
pip install git+https://github.com/v-spassky/drainage.git
```

### Usage

```python
from drainage import piped, filtered, collect

@piped
def add_one(x):
    return x + 1

@filtered
def is_even(x):
    return x % 2 == 0

result = [1, 2, 3, 4] | add_one | is_even | collect()
print(result)  # Output: [2, 4]
```
