import operator
import re

PATTERN_REGEX = re.compile(r'([\-\w]+)([\!<>=]{1,2})(.+)')
_OPERATIONS = {
            '=': operator.eq,
            '==': operator.eq,
            '!=': operator.ne,
            '<': operator.lt,
            '<=': operator.le,
            '>': operator.gt,
            '>=': operator.ge
        }


class Comparer:
    def __init__(self, expression: str):
        m = PATTERN_REGEX.match(expression)
        self._expression = expression
        self._parameter = m.group(1)
        self._operator = _OPERATIONS[m.group(2)]
        try:
            _expected = int(m.group(3))
        except ValueError:
            try:
                _expected = float(m.group(3))
            except ValueError:
                _expected = m.group(3)
        self._expected = _expected

    @property
    def parameter(self):
        return self._parameter

    def __str__(self):
        return self._expression

    def __call__(self, value):
        return self._operator(value, self._expected)
