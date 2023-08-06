import random


class Dummy:
    def __init__(self, valids, invalids):
        self._valids_ = valids
        self._invalids_ = invalids
    
    def _generate(generator, count, exhaustive):
        if isinstance(generator, list) or isinstance(generator, tuple):
            if exhaustive or count >= len(generator):
                return [x for x in generator]
            else:
                return random.sample(generator, count)
        else:
            return [generator() for _ in range(count)]
    
    def valids(self, count=1, exhaustive=False):
        return Dummy._generate(self._valids_, count, exhaustive)
    
    def invalids(self, count=1, exhaustive=False):
        return Dummy._generate(self._invalids_, count, exhaustive)
    
    def valid(self, value, raise_error=False):
        raise NotImplementedError("valid() not implemented.")

    def examples(self):
        return {
            "valid": self.valids(),
            "invalid": self.invalids(),
        }
    
    def equals(self, v1, v2):
        if v1 is None and v2 is None:
            return True
        if v1 is None or v2 is None:
            return False
        return self._equals(v1, v2)

    def _equals(self, v1, v2):
        return v1 == v2