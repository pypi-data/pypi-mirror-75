from quiq.test import ExceptionWrapper

# Types
Symbol = str
Number = (int, float)
Bool   = bool

# Maps functions to their implementation
environment = {
    # Basics
    'list' : lambda *args: list(args),
    'quote': 'quote',
    'car'  : lambda L    : L[0],
    'cdr'  : lambda L    : list(L[1:]),

    # Operators
    'and' : lambda *args: reduce(lambda x, y: x and y, args),
    'or'  : lambda *args: reduce(lambda x, y: x or  y, args),
    '=='  : lambda x, y : x == y,
    '!='  : lambda x, y : x != y,
    '<'   : lambda x, y : x <  y,
    '<='  : lambda x, y : x <= y,
    '>'   : lambda x, y : x >  y,
    '>='  : lambda x, y : x >= y,
    'isin': lambda x, y : x in y,
    'throws': lambda err, err_class: isinstance(err, err_class),
}


class UnknownSymbolError(Exception): ...


def evaluate(texp, env=environment):
    "Evaluate an expression in an environment."
    if isinstance(texp, Symbol):
        if texp not in env: raise UnknownSymbolError(f"Unknown symbol: `{texp}`")
        return env[texp]
    elif isinstance(texp, (Number, Bool)):
        return texp
    elif isinstance(texp, ExceptionWrapper):
        return texp.err_type

    # Functions
    else:
        func = evaluate(texp[0], env)
        if func == 'quote': return texp[1]
        args = [evaluate(t, env) for t in texp[1:]]

        # Try calling the function. Catch exception and return them for throw
        # to catch
        try:
            result = func(*args)
        except Exception as e:
            result = e
        return result
