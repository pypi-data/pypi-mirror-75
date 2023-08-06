import exrex
import math
import pytest
import random
import sys


from .dummy import Dummy
from .util import _test_valid_args, _test_invalid_args



class Number(Dummy):
    def __init__(self, minimum=None, maximum=None, multiple_of=None,
                 exclusive_minimum=False, exclusive_maximum=False):
        if minimum is not None and maximum is not None and minimum > maximum:
            raise ValueError("minimum is greater than maximum")
        if exclusive_minimum or exclusive_maximum:
            if minimum is not None and maximum is not None and minimum == maximum:
                raise ValueError(
                    "minimum and maximum cannot be equal and excluded")
        
        self.minimum = minimum
        self.maximum = maximum
        if multiple_of is not None:
            if minimum is not None and minimum % multiple_of != 0:
                if maximum is not None and maximum % multiple_of != 0:
                    if math.floor(minimum / multiple_of) == math.floor(maximum / multiple_of):
                        raise ValueError(
                            "Invalid multiple_of for minimum / maximum")
        self.multiple_of = multiple_of
        self.exclusive_minimum = exclusive_minimum
        self.exclusive_maximum = exclusive_maximum
        
        super().__init__(self._valids, self._invalids())
    
    def valid(self, value, raise_error=False):
        if not isinstance(value, float) and not isinstance(value, int):
            if raise_error:
                raise ValueError("{} is not a float but {}".format(value, type(value)))
            return False
        if self.minimum and (
            (self.exclusive_minimum and value <= self.minimum) or
            (not self.exclusive_minimum and value < self.minimum)
        ):
            if raise_error:
                raise ValueError("{} < {}".format(value, self.minimum))
            return False
        if self.maximum and (
            (self.exclusive_maximum and value >= self.maximum) or
            (not self.exclusive_maximum and value > self.maximum)
        ):
            if raise_error:
                raise ValueError("{} > {}".format(value, self.maximum))
            return False
        if self.multiple_of and (
            (value % self.multiple_of) > sys.float_info.epsilon
            and
            (value % self.multiple_of) - self.multiple_of > sys.float_info.epsilon
        ) != 0:
            if raise_error:
                print("v, m:", value, self.multiple_of)
                print(value % self.multiple_of)
                print((value % self.multiple_of) - self.multiple_of)
                print((value % self.multiple_of) - self.multiple_of < sys.float_info.epsilon)
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
        elif self.multiple_of is not None:
            start = min(10 * self.multiple_of, 0.0)
            end = max(10 * self.multiple_of, 0.0)
        else:
            start = 0.0
            end = 1.0

        counter = 0
        while True:
            if counter > 100:
                raise StopIteration(
                    "Hit minimum or maximum more than 100 times.")
            
            if self.multiple_of is None:
                v = random.uniform(start, end)
            else:
                start_ = int(math.ceil(start / self.multiple_of))
                end_ = int(math.floor(end / self.multiple_of))
                v = random.randint(start_, end_) * self.multiple_of
            
            if self.exclusive_minimum and v == start:
                counter += 1
                continue
            if self.exclusive_maximum and v == end:
                counter += 1
                continue
            
            return v

    def _invalids(self):
        invalids = [4.2, exrex.getone("[a-z]{5}")]
        if self.minimum is not None:
            invalids.append(self.minimum - 1.0)
        if self.maximum is not None:
            invalids.append(self.maximum + 1)
        return invalids

    def __str__(self):
        l = "(" if self.exclusive_minimum else "["
        r = ")" if self.exclusive_maximum else "]"
        return "Number: {}{}, {}{}".format(l, self.minimum, self.maximum, r)


def test_number():
    _test_valid_args(Number, [
        [1.1, 10.3, 2.5], [-20, -10.0],
        [-16.2, -14, 0.4], [-17.6, -14, 8.8]
    ])

    _test_invalid_args(Number, [
        [10, 1], [-10, -11],
        [1, 10, 100], [5, 10, 12],
        [-15, -10, 8]
    ])

    for count in range(10):
        assert len(Number().valids(count, True)) == count
        assert len(Number().valids(count, False)) == count
    
    assert Number(3, 3).valids() == [3]
    assert Number(14.1, 15.2, 1.51).valids() == [15.1]
    for i in range(20):
        assert Number(1, 1.6, 0.3).valids()[0] in [1.2, 1.5]
        assert Number(-4, -2, 1).valids()[0] in [-4, -3, -2]
    
    i = Number(10, 12, 0.4)
    for v in list(range(6)):
        v = 10.0 + v * 0.4
    for v in i.valids(10):
        assert i.valid(v, True)
    for v in [-10, 9.9999, 12.0001, 234.2] + i.invalids(1, True):
        with pytest.raises(ValueError):
            i.valid(v, True)
    i = Number(10, 12, 0.4, True, True)
    for v in [10, 12]:
        with pytest.raises(ValueError):
            i.valid(v, True)
