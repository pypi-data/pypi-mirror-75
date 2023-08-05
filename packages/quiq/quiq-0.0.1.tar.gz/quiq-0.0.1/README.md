# quiq
quiq is a simple and lightweight unit testing framework for for exploratory and
prototyping coding. quiq allows unit tests to be written right before functions
are declared in order to make a much more natural test/develop workflow in the
spirit of TDD.

### Example:
```python
@TestCase(
    F(6, 5).isin(list(range(2,50))),
    F(6, 5) == 11,
    F(1,2) == 51,
    F(1,2).throws()
)
def add(x, y):
    if x == 1: raise ValueError("No 1s!")
    return x + y
```

```
Test Case: add
✅  Original: add(6, 5) isin [2, 3, 4, 5...47, 48, 49]
    Expanded:        11 isin [2, 3, 4, 5...47, 48, 49]

✅  Original: add(6, 5) == 11
    Expanded:        11 == 11

❌  Original: add(1, 2) == 51
    Expanded: ValueError('No 1s!')

✅  Original: add(1, 2) throws Exception
    Expanded: ValueError('No 1s!')
```
