import pytest

def _test_valid_args(constr, argss):
    for args in argss:
        if isinstance(args, dict):
            print("VALID:", args.keys())
            x = constr(**args)
        elif isinstance(args, list):
            print("VALID:", [str(x) for x in args])
            x = constr(*args)
        else:
            raise ValueError("Invalid args type: {}".format(type(args)))
        x.valids()
        x.invalids()
        str(x)


def _test_invalid_args(constr, argss):
    for args in argss:
        if isinstance(args, dict):
            print("INVALID:", args.keys())
            with pytest.raises(Exception):
                x = constr(*args)
        elif isinstance(args, list):
            print("INVALID:", [str(x) for x in args])
            with pytest.raises(Exception):
                x = constr(**args)
        else:
            raise ValueError("Invalid args type: {}".format(type(args)))
