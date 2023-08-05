# A constant to represent the test being called
_F = 'F'

class ExceptionWrapper:
    """Wraps an Exception type so it can be type checked"""
    def __init__(self, err_type):
        self.err_type = err_type
    def __repr__(self):
        return repr(self.err_type)[8:-2]

class Test():
    """The basic unit for a test. It holds:
    - The function thats being tested
    - Arguments used to call the function
    - The operator to compare outputs
    - The expected value when the function is evaluated
    """
    def __init__(self, *args):
        self.function = _F          # The function to test
        self.args     = list(args)  # Args to evaluate the function with
        self.operator = None        # How we expect to interpret the value of the function
        self.expected = None        # What we expect to happen when the function is called

    def __repr__(self):
        res =  f"{self.function}("
        res += ', '.join([str(a) for a in self.args])
        res += ")"
        res += f" {self.operator}"
        res += f" {self.expected}"
        return res

    """ ----------------------------------------------------------------------
    OPERATORS
    -----------------------------------------------------------------------"""
    def __eq__(self, expected): self.operator, self.expected = '==', expected; return self
    def __ne__(self, expected): self.operator, self.expected = '!=', expected; return self
    def __lt__(self, expected): self.operator, self.expected = '<',  expected; return self
    def __le__(self, expected): self.operator, self.expected = '<=', expected; return self
    def __gt__(self, expected): self.operator, self.expected = '>',  expected; return self
    def __ge__(self, expected): self.operator, self.expected = '>=', expected; return self

    def isin(self, other):
        self.operator, self.expected = 'isin', ['list', *other]
        return self

    def throws(self, err=None):
        self.operator = 'throws'
        self.expected = ExceptionWrapper(err) if err else ExceptionWrapper(Exception)
        return self

# Alias
F = Test
