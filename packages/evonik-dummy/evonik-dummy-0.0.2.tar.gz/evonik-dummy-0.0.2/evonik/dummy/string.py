from enum import Enum as Enum_
import exrex
import pytest
import random
import re


from .dummy import Dummy
from .util import _test_valid_args, _test_invalid_args


class StringPattern(Enum_):
    CHARS: "[A-Za-z]{8,16}"
    CHARS_NUMBERS: "[A-Za-z0-9]{8,16}"
    CHARS_NUMBERS_SPACES: "[A-Za-z0-9 ]{8,16}"
    CHAR_CHARS_NUMBERS_CHAR: "[A-Za-z][A-Za-z0-9]{6,14}[A-Za-z]"
    CHAR_CHARS_SPACES_CHAR: "[A-Za-z][A-Za-z ]{6,14}[A-Za-z]"
    CHAR_CHARS_NUMBERS_SPACES_CHAR: "[A-Za-z][A-Za-z0-9 ]{6,14}[A-Za-z]"

class String(Dummy):
    def __init__(self, min_length=None, max_length=None, pattern=None, invalid_pattern=None):
        if min_length and min_length < 0:
            raise ValueError("Min length cannot be smaller than 0 but is {}.".format(min_length))
        if max_length and max_length < 0:
            raise ValueError("Max length cannot be smaller than 0 but is {}.".format(max_length))
        if min_length and max_length and min_length > max_length:
            raise ValueError("Min length cannot be larger than max length.")
        if invalid_pattern and not pattern:
            raise ValueError("Must specify pattern with invalid_pattern")
        
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = pattern
        self.pattern_ = re.compile(pattern) if pattern else None
        self.invalid_pattern = invalid_pattern
        
        super().__init__(self._valids, self._invalids())
    
    def valid(self, value, raise_error=False):
        if not isinstance(value, str):
            if raise_error:
                raise ValueError("{} is not a string but {}".format(value, type(value)))
            return False
        if self.min_length and len(value) < self.min_length:
            if raise_error:
                raise ValueError("{} < {}".format(value, self.min_length))
            return False
        if self.max_length and len(value) > self.max_length:
            if raise_error:
                raise ValueError("{} > {}".format(value, self.max_length))
            return False
        if self.pattern_ and not self.pattern_.match(value):
            if raise_error:
                raise ValueError("{} does not match the pattern {}".format(value, self.pattern))
        return True

    def _valids(self):
        if self.pattern:
            return exrex.getone(self.pattern)
        if self.min_length is None and self.max_length is None:
            length = random.randint(8, 16)
        elif self.max_length is None:
            length = random.randint(self.min_length,
                                    2 * self.min_length)
        elif self.min_length is None:
            length = random.randint(math.floor(self.max_length / 2),
                                    self.max_length)
        else:
            length = random.randint(self.min_length, self.max_length)
        return exrex.getone("[A-Za-z0-9]{{{}}}".format(length))

    def _invalids(self):
        invalids = [
            random.randint(0, 100),
            random.random()
        ]
        if self.invalid_pattern:
            invalids.append(exrex.getone(self.invalid_pattern))
        return invalids

    def __str__(self):
        return "String: {} ({}, {})".format(self.pattern, self.min_length, self.max_length)


def test_string():
    _test_valid_args(String, [
        [1, 10], [20, 20],
        {"pattern": "[a-z]{10,20}"},
        {"pattern": "[a-z]{10,20}", "invalid_pattern": "[a-z]{9}"}
    ])

    _test_invalid_args(String, [
        [-3, 10], [10, 9],
        {"invalid_pattern": "[a-z]{9}"}
    ])
    
    for x in range(0,30):
        assert len(String(x, x).valids()[0]) == x
    for a in range(20):
        for b in range(a, 30):
            assert a <= len(String(a, b).valids()[0]) <= b
    
    for i in range(10):
        assert String(i, i, "0123456789").valids()[0] == "0123456789"
    assert len(String(8, 8, "[0-9]{4}").valids()[0]) == 4
    assert len(String(1, 1, "abcd[0-9]{4}").valids()[0]) == 8
    s = String(pattern="aaa", invalid_pattern="abc")
    assert "aaa" in s.valids(1, True)
    assert "abc" in s.invalids(1, True)
