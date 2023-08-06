# Python implementation of `is_thirteen`  by [jezen](https://github.com/jezen/is-thirteen)
A python package(pypi) to check whether the input is `13` or not.

### Install
```shell script
pip install --upgrade is_thirteen
```

### Usage
```python
from is_thirteen import Number, Str

# basic skills
Number(13).thirteen()                   # True
Number(12.8).roughly().thirteen()       # True
Number(6).within(10).thirteen()         # True

# math operations
Number(4).plus(5).thirteen()            # False
Number(12).plus(1).thirteen()           # True
Number(4).minus(7).thirteen()           # False
Number(14).minus(1).thirteen()          # True
Number(1).times(8).thirteen()           # False
Number(26).divides(2).thirteen()        # True

# spelling and chemistry skillz
Str("ThirTEEn").thirteen()              # True
Str("nEETrihT").backwards().thirteen()  # True
```
