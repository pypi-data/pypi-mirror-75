import logging

from quiq.evaluate import evaluate, environment

class TestCase:
    """A Test case - it acts as the interface to the user and constructs and
    runs tesp code"""
    def __init__(self, *args):
        # Optional: The first argument can be a description, everything else
        # is an unevalauted texp.
        self.desc = None

        if isinstance(args[0], str):
            self.desc = args[0]
            args = args[1:]
        self.tests = args

    def __call__(self, func):
        self.func = func
        if not self.desc: self.desc = func.__name__

        # Bind the given function to 'F'
        env = environment.copy()
        env['F'] = self.func

        # Tesp code to run tests and return test results that look like:
        # (didPass Test actual)
        tesp = ['list']
        for test in self.tests:
            op, F, args, expected = test.operator, test.function, test.args, test.expected
            test = [op, [F, *args], expected]
            actual  = [F, *args]
            # Append a test result
            tesp += [['list', test, ['quote', test], actual]]

        results = evaluate(tesp, env)

        self._report(results)

        return func

    def _report(self, results):
        logging.basicConfig(format='%(message)s')
        log = logging.getLogger(__name__)

        log.warning(f"Test Case: {self.desc}")

        for didPass, (operator, (F, *args), expected), actual in results:
            line = "✅" if didPass else "❌"

            func_name = self.func.__name__
            args = ', '.join([str(a) for a in args])

            # Process lists specially:
            if isinstance(expected, list):
                expected = ', '.join([str(e) for e in expected[1:]]) # Remove the first element, 'list'
                expected = f"[{expected[:10]}...{expected[-10:]}]"

            line += f"  Original: {func_name}({args}) {operator} {expected}\n"
            if isinstance(actual, Exception):
                line += f"    Expanded: {repr(actual)}"
            else:
                line += f"    Expanded: {' ' * (len(func_name + args)) }{actual} {operator} {expected}"
            line += '\n'
            log.warning(line)
