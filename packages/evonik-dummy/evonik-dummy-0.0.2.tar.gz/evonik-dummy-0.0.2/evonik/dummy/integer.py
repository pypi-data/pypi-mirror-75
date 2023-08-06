import exrex
import math
import pytest
import random


from .dummy import Dummy
from .util import _test_valid_args, _test_invalid_args


class Integer(Dummy):
    def __init__(self, minimum=None, maximum=None, multiple_of=None):
        if minimum is not None and maximum is not None and minimum > maximum:
            raise ValueError("minimum is greater than maximum")
        
        self.minimum = minimum
        self.maximum = maximum
        if multiple_of is not None:
            if minimum % multiple_of != 0:
                if minimum % multiple_of != 0:
                    if math.floor(minimum / multiple_of) == math.floor(maximum / multiple_of):
                        raise ValueError(
                            "Invalid multiple_of for minimum / maximum")
        self.multiple_of = multiple_of
        
        super().__init__(self._valids, self._invalids())
    
    def valid(self, value, raise_error=False):
        if not isinstance(value, int):
            if raise_error:
                raise ValueError("{} is not an int but {}".format(value, type(value)))
            return False
        if self.minimum and value < self.minimum:
            if raise_error:
                raise ValueError("{} < {}".format(value, self.minimum))
            return False
        if self.maximum and value > self.maximum:
            if raise_error:
                raise ValueError("{} > {}".format(value, self.maximum))
            return False
        if self.multiple_of and (value % self.multiple_of) != 0:
            if raise_error:
                raise ValueError("{} is not multiple of {}".format(value, self.multiple_of))
            return False
        return True

    def _valids(self):
        if self.minimum is not None and self.maximum is not None:
            start = self.minimum
            end = self.maximum
        elif self.minimum is not None:
            start = self.minimum
            end = self.minimum + 10
        elif self.maximum is not None:
            start = self.maximum - 10
            end = self.maximum
        else:
            start = 1
            end = 100
        if self.multiple_of is None:
            return random.randint(start, end)
        else:
            a = int(math.ceil(start / self.multiple_of)) * self.multiple_of
            b = int(math.floor(end / self.multiple_of)) * self.multiple_of
            return random.randrange(a, b+1, self.multiple_of)

    def _invalids(self):
        invalids = [4.2, exrex.getone("[a-z]{5}")]
        if self.minimum is not None:
            invalids.append(self.minimum - 1)
        if self.maximum is not None:
            invalids.append(self.maximum + 1)
        return invalids

    def __str__(self):
        return "Number: [{}, {}]".format(self.minimum, self.maximum)


def test_integer():
    _test_valid_args(Integer, [
        [1, 10, 2], [-20, -10],
        [-16, -14, 5], [-16, -14, 8]
    ])

    _test_invalid_args(Integer, [
        [10, 1], [-10, -11],
        [1, 10, 100], [5, 10, 12],
        [-15, -10, 8]
    ])

    for count in range(10):
        assert len(Integer().valids(count, True)) == count
        assert len(Integer().valids(count, False)) == count
    assert Integer(1, 5, 3).valids() == [3]
    assert Integer(10, 15, 4).valids() == [12]
    assert Integer(-4, -4).valids() == [-4]
    for i in range(20):
        assert Integer(1, 6, 3).valids()[0] in [3, 6]
    i = Integer(10, 20, 2)
    for v in list(range(10, 22, 2)) + i.valids(10):
        assert i.valid(v, True)
    for v in [-10, 9, 21, 234, 11, 0.4] + i.invalids(1, True):
        with pytest.raises(ValueError):
            i.valid(v, True)