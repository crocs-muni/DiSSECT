from sage.all import ZZ, ecm, factor, sqrt
from sage.parallel.decorate import fork


class Factorization:
    def __init__(self, x, use_ecm=False, timeout_duration=20, factorization=None):
        self._value = x
        self._square = None
        self._squarefree = None
        self._square_root = None
        self._factorization = None
        self._timeout = False
        self._use_ecm = use_ecm
        self._timeout_duration = timeout_duration
        self._unit = 1 if x >= 0 else -1
        self.set_factorization(factorization)

    def value(self):
        return self._value

    def timeout(self):
        return self._timeout

    def use_ecm(self):
        return self._use_ecm

    def timeout_duration(self):
        return self._timeout_duration

    def timeout_message(self):
        if not self._timeout:
            return "No timeout!"
        return self._factorization

    def factorization(self, unpack=True):
        if self._timeout:
            return self.timeout_message()
        if unpack:
            return [i for (i, e) in self._factorization for _ in range(e)]
        return self._factorization

    def set_factorization(self, factorization):
        if factorization is not None:
            self._factorization = factorization
            if isinstance(factorization, str):
                self._timeout = True
        elif self._use_ecm:
            factors = timeout(ecm.factor, [self._value], timeout_duration=self._timeout_duration)
            if isinstance(factors, str):
                self._timeout = True
                self._factorization = factors
            else:
                self._factorization = [(i, factors.count(i)) for i in set(factors)]
        else:
            factors = timeout(factor, [self._value], timeout_duration=self._timeout_duration)
            if isinstance(factors, str):
                self._timeout = True
                self._factorization = factors
            else:
                self._factorization = list(factors)

    def squarefree(self):
        if self._squarefree is not None:
            return self._squarefree
        if self._timeout:
            return self._factorization
        squarefree = 1
        for p, e in self._factorization:
            if e % 2 == 1:
                squarefree *= p
        self._squarefree = self._unit * squarefree
        return self._squarefree

    def square(self):
        if self._square is not None:
            return self._square
        if self._timeout:
            return self._factorization
        self._square = ZZ(self._value // self.squarefree())
        return self._square

    def square_root(self):
        if self._square_root is not None:
            return self._square_root
        if self._timeout:
            return self._factorization
        self._square_root = ZZ(sqrt(self.square()))
        return self._square_root

    def cm_squarefree(self):
        if self._timeout:
            return self._factorization
        cm = self.squarefree() * 4 if self.squarefree() % 4 != 1 else self.squarefree()
        return cm

    def cm_conductor(self):
        if self._timeout:
            return self._factorization
        return ZZ(sqrt(self._value // self.cm_squarefree()))

    def __add__(self, other):
        value = self.value() * other.value()
        if self.timeout() or other.timeout():
            return Factorization(value, factorization=self.timeout_message())
        other_factors = dict(other.factorization(False))
        factors = [(p, e + other_factors.get(p, 0)) for p, e in self.factorization(False)]
        self_primes = set(self.factorization())
        factors += [i for i in other.factorization(False) if not i[0] in self_primes]
        return Factorization(value, factorization=sorted(factors, key=lambda x: x[0]))


def customize_curve(curve):
    db_curve = {"name": "joe"}
    q = curve.base_field().order()
    order = factor(curve.order())[-1][0]
    db_curve["order"] = order
    db_curve["category"] = "my"
    db_curve["form"] = "Weierstrass"

    def my_hex(x):
        return format(ZZ(x), "#04x")

    if q % 2 != 0:
        db_curve["params"] = {
            "a": {"raw": my_hex(curve.a4())},
            "b": {"raw": my_hex(curve.a6())},
        }
        db_curve["field"] = {"type": "Prime", "p": my_hex(q), "bits": q.nbits()}
    else:
        db_curve["params"] = {
            "a": {"raw": my_hex(curve.a2())},
            "b": {"raw": my_hex(curve.a6())},
        }
        db_curve["field"] = {"type": "Binary"}
        db_curve["field"]["poly"] = [
            {"power": deg, "coeff": my_hex(coef)}
            for deg, coef in curve.base_field().polynomial().dict().items()
        ]
        db_curve["field"]["bits"] = curve.base_field().polynomial().degree()
        db_curve["field"]["degree"] = curve.base_field().polynomial().degree()
        db_curve["field"]["basis"] = "poly"
    db_curve["desc"] = ""
    db_curve["cofactor"] = curve.order() // order
    db_curve["generator"] = None
    return db_curve


def timeout(func, args=(), kwargs=None, timeout_duration=10):
    """Stops the function func after 'timeout_duration' seconds, taken from
    https://ask.sagemath.org/question/10112/kill-the-thread-in-a-long-computation/."""
    if kwargs is None:
        kwargs = {}

    @fork(timeout=timeout_duration, verbose=False)
    def my_new_func():
        return func(*args, **kwargs)

    return my_new_func()
