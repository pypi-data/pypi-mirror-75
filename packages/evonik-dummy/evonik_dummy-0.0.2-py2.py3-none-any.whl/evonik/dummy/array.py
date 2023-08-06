import pytest
import random

from .dummy import Dummy
from .integer import Integer
from .string import String
from .util import _test_valid_args, _test_invalid_args


class Array(Dummy):
    def __init__(self, datatype, min_items=None, max_items=None, unique_items=False):
        if min_items is not None and min_items < 0:
            raise ValueError("min_items must be creater than 0, not {}".format(mi_items))
        if max_items is not None and max_items < 0:
            raise ValueError("maxItems must be creater than 0, not {}".format(max_items))
        if min_items is not None and max_items is not None and min_items > max_items:
            raise ValueError("min_items ({}) cannot be larger than maxItems ({}).").format(min_items, max_items)
        
        self.datatype = datatype
        self.min_items = min_items
        self.max_items = max_items
        self.unique_items = unique_items
        
        super().__init__(self._valids, self._invalids())
    
    def valid(self, value, raise_error=False):
        if self.min_items and len(value) < self.min_items:
            if raise_error:
                raise ValueError("{} < {}".format(len(value), self.min_items))
            return False
        if self.max_items and len(value) > self.max_items:
            if raise_error:
                raise ValueError("{} > {}".format(len(value), self.max_items))
            return False
        if self.unique_items:
            uniques = set([str(x) for x in value])
            if len(value) != len(uniques):
                if raise_error:
                    raise ValueError("{} has duplicate elements".format(value))
                return False
        for v in value:
            if not self.datatype.valid(v, raise_error):
                return False
        return True
    
    def _valids(self):
        length = random.randint(*self._valid_length_range())
        return self._valid_list(length)
    
    def _valid_list(self, length):
        if not self.unique_items:
            return [self.datatype.valids(1)[0] for _ in range(length)]
        else:
            valids = []
            duplicates = 0
            while len(valids) < length:
                v = self.datatype.valids(1)[0]
                if v not in valids:
                    valids.append(v)
                else:
                    duplicates += 1
                    if duplicates > 100 * length:
                        raise ValueError("Generated {} duplicate items. ".format(duplicates) +
                                         "Current list size: {} / {}.".format(len(valids), length) +
                                         "Does the datatype generate enough unique values?")
            return valids
    
    def _invalids(self):
        invalids = []
        # too short
        if self.min_items and self.min_items > 0:
            invalids.append(self._valid_list(self.min_items - 1))
        # too long
        if self.max_items:
            invalids.append(self._valid_list(self.max_items + 1))
        # invalid item
        if self._valid_length_range()[1] > 0:
            inv = self.datatype.invalids()
            if len(inv) > 0:
                invalids.append(self._valid_list(self._valid_length_range()[1]))
                invalids[-1][-1] = inv[0]
        # duplicate items
        if self.unique_items:
            if self._valid_length_range()[1] > 1:
                invalids.append(self._valid_list(self._valid_length_range()[1]))
                invalids[-1][-1] = invalids[-1][0]
        return invalids
    
    def _valid_length_range(self):
        if self.min_items is not None and self.max_items is not None:
            return self.min_items, self.max_items
        elif self.min_items is not None:
            return self.min_items, self.min_items + 10
        elif self.max_items is not None:
            return 0, self.max_items
        else:
            return 0, 10
    
    def __str__(self):
        return "Array: {}".format(str(self.datatype))

    def _equals(self, spec, res):
        if len(spec) != len(res):
            raise ValueError("Arrays have different lengths.")
        for v1, v2 in zip(spec, res):
            self.datatype.equals(v1, v2)
        return True


def test_array():
    _test_valid_args(Array, [
        [String()], [String(), 3],
        [String(), 5, 8], [String(), 5, 8, True],
        [Integer(1, 3), 2, 2, True]
    ])

    _test_invalid_args(Array, [
        [String(), -1], [String(), 3, -2],
        [String(), -2, -1], [String(), 6, 3],
        [Integer(1, 10), 11, 11, True]
    ])

    assert len(Array(Integer(), 3, 3).valids()[0]) == 3
    assert len(Array(Integer(), 10, 10).valids()[0]) == 10
    for i in range(10):
        assert 4 < len(Array(String(), 5, 9).valids()[0]) < 10
    for i in range(10):
        assert len(set(Array(Integer(1, 100), 10, 10, True).valids()[0])) == 10
    for unique_items in [True, False]:
        a = Array(Integer(), 5, 10, unique_items)
        for v in a.valids(10):
            assert a.valid(v, True)
        for v in a.invalids(1, True):
            with pytest.raises(ValueError):
                a.valid(v, True)
