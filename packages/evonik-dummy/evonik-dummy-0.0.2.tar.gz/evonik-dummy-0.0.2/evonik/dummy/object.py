import exrex
import pytest
import re


from .dummy import Dummy
from .string import String
from .util import _test_valid_args, _test_invalid_args


class Object(Dummy):
    def __init__(self,
                 props,
                 required=None,
                 forbid_additional_props=False,
                 check_invalid_props=False):
        self.props = props
        if len(props) == 0:
            raise ValueError("Must specify at least on prop.")
        self.required = required if required else []
        self.forbid_additional_props = forbid_additional_props
        self.check_invalid_props = check_invalid_props
        super().__init__(self._valids, None)
        self._invalids_ = self._invalids()
    
    def valid(self, value, raise_error=False):
        if self.forbid_additional_props:
            for k in value:
                if k not in self.props:
                    if raise_error:
                        raise ValueError("unknown property: {}".format(k))
                    return False
        for k in self.required:
            if k not in value:
                if raise_error:
                    raise ValueError("property {} is required but  isssing".format(k))
                return False
        for k,v in value.items():
            if not self.props[k].valid(v, raise_error):
                return False
        return True
    
    def _valids(self):
        return {
            k: v.valids(1, False)[0]
            for k,v in self.props.items()
        }
    
    def _invalids(self):
        invalids = []
        for k in self.required:
            invalids.append(self.valids()[0])
            del invalids[-1][k]
        if self.check_invalid_props:
            for k,p in self.props.items():
                inv = self.props[k].invalids(1, False)
                if len(inv) > 0:
                    invalids.append(self.valids()[0])
                    invalids[-1][k] = inv[0]
        if self.forbid_additional_props:
            invalids.append(self.valids()[0])
            k = exrex.getone("[a-zA-Z0-9]{16,32}")
            invalids[-1][k] = k
        return invalids
    
    def __str__(self):
        return "Object: {}".format(list(self.props.keys()))

    def _equals(self, spec, res):
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        def to_key(original):
            return pattern.sub('_', original).lower()
        spec = spec if isinstance(spec, dict) else spec.to_dict()
        res = res if isinstance(res, dict) else res.to_dict()
        spec = {to_key(k):v for k,v in spec.items()}
        res = {to_key(k):v for k,v in spec.items()}
        props = {to_key(k):v for k,v in self.props.items()}
        for k, v in spec.items():
            if k not in props:
                raise KeyError(
                    "Key {} not present in Object's definition.".format(k))
            if k not in res:
                raise KeyError(
                    "Key {} not present in result.".format(k))
            if not props[k].equals(v, res[k]):
                raise ValueError("Properties for key {} do not match ({} != {})".format(k, v, res[k]))
        return True


def test_object():
    _test_valid_args(Object, [
        [{"a": String(), "b": String()}]
    ])
    _test_invalid_args(Object, [
        [], [{}]
    ])

    o = Object({
        "a": String(pattern="aaa"),
        "b": String(pattern="bbb"),
    })
    assert o.valids()[0] == {"a": "aaa", "b": "bbb"}
    props = {
        "a": String(pattern="[a-z]{5}", invalid_pattern="aaa"),
        "b": String(pattern="[A-Z]{10}", invalid_pattern="bbb"),
    }
    flags = {
        "check_invalid_props": True,
        "forbid_additional_props": False,
    }
    for i in range(10):
        o = Object(props, **flags)
        for v in o.valids():
            assert o.valid(v, True)
    for i in range(10):
        o = Object(props, **flags)
        for v in o.invalids(1, True):
            with pytest.raises(ValueError):
                print(v)
                o.valid(v, True)
