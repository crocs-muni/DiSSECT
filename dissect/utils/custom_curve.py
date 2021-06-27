from sage.all import EllipticCurve, ZZ, GF, Integers, factor  # import sage library
from dissect.utils.curve_form import dict_to_poly, CurveForm
from dissect.traits.trait_interface import timeout


class CustomCurve:
    """Class for unified representation of curves from databases"""

    def __init__(self, db_curve):
        self._name = db_curve["name"]
        self._order = ZZ(db_curve["order"])
        self._category = db_curve["category"]
        self._params = db_curve["params"]
        self._cofactor = ZZ(db_curve["cofactor"])
        self._cardinality = self._order * self._cofactor
        self._nbits = self._order.nbits()
        self._field = None
        self._field_type = None
        self._q = None
        self._form = None
        self._ec = None
        self.set_field(db_curve["field"])
        self.set_form(db_curve["form"])
        self.set_ec()
        # Non-mandatory attributes:
        self._trace = None
        self._j_invariant = None
        self._embedding_degree = None
        self._cm_discriminant = None
        self._frobenius_disc_factorization = None
        self.set_properties(db_curve)
        self._generator = None
        self.set_generator(db_curve)
        self._desc = db_curve.get("desc", None)
        self._seed = db_curve.get("simulation", {}).get("seed", None)

    def name(self):
        return self._name

    def order(self):
        return self._order

    def category(self):
        return self._category

    def params(self):
        return self._params

    def cofactor(self):
        return self._cofactor

    def cardinality(self):
        return self._cardinality

    def nbits(self):
        return self._nbits

    def field(self):
        return self._field

    def field_type(self):
        return self._field_type

    def q(self):
        return self._q

    def form(self):
        return self._form

    def ec(self):
        return self._ec

    def description(self):
        return self._desc

    def seed(self):
        return self._seed

    def is_over_binary(self):
        return self._field.characteristic() % 2 == 0

    def a(self):
        return self._form.a()

    def b(self):
        return self._form.b()

    def generator(self):
        return self._generator

    def embedding_degree(self):
        if self._embedding_degree is None:
            self._embedding_degree = (Integers(self._order)(self._q)).multiplicative_order()
        return self._embedding_degree

    def trace(self):
        return self._trace

    def j_invariant(self):
        j = self._j_invariant
        if self.is_over_binary():
            j = self._field(j).integer_representation()
        return j

    def cm_discriminant(self):
        if self._cm_discriminant is None:
            d = squarefree_and_factorization(self.trace() ** 2 - 4 * self._q)
            if isinstance(d, str):
                return self._cm_discriminant
            self._cm_discriminant = 4 * d[0] if d[0] % 4 != 1 else d[0]
            self._frobenius_disc_factorization = d[1]
        return self._cm_discriminant

    def frobenius_disc_factorization(self):
        self.cm_discriminant()
        if self._frobenius_disc_factorization is None:
            self._frobenius_disc_factorization = timeout(factor, [self.trace() ** 2 - 4 * self._q])
        return self._frobenius_disc_factorization

    def is_over_extension(self):
        return not (self.field().is_prime_field() or self.is_over_binary())

    def is_over_prime(self):
        return self.field().is_prime_field()

    def set_field(self, field_dict):
        self._field_type = field_dict["type"]
        if field_dict["type"] == "Prime":
            p = ZZ(field_dict["p"])
            self._field = GF(p, proof=False)
            self._q = p
        else:
            base = ZZ(2) if field_dict["type"] == "Binary" else ZZ(field_dict["base"])
            degree = ZZ(field_dict["degree"])
            modulus = dict_to_poly(field_dict["poly"], GF(base)["w"])
            self._field = GF(base ** degree, "w", modulus, proof=False)
            self._q = base ** degree

    def set_form(self, form_desc):
        if form_desc in ["Edwards", "TwistedEdwards"]:
            a = 1 if form_desc == "Edwards" else self._params["a"]
            d = self._params["d"]
            self._form = CurveForm(self._field, {"form": "edwards", "a": a, "d": d})
        if form_desc == "Montgomery":
            a, b = self._params["a"], self._params["b"]
            self._form = CurveForm(self._field, {"form": "montgomery", "a": a, "b": b})
        if form_desc == "Weierstrass":
            a, b = self._params["a"], self._params["b"]
            self._form = CurveForm(self._field, {"form": "weierstrass", "a": a, "b": b})

    def set_ec(self):
        if self.is_over_binary():
            self._ec = EllipticCurve(self.field(), [1, self.a(), 0, 0, self.b()])
        else:
            self._ec = EllipticCurve(self.field(), [self.a(), self.b()])
        self._ec.set_order(self._cardinality, num_checks=0)

    def set_generator(self, db_curve):
        try:
            generator = db_curve['generator']
            x, y = generator["x"], generator["y"]
            to_skip = ["", None]
            if x not in to_skip and y not in to_skip:
                x, y = self.form().point(x, y)
                self._generator = self._ec(x, y)
        except (KeyError, TypeError):
            pass

    def set_properties(self, db_curve):
        try:
            properties = db_curve['properties']
            self._cm_discriminant = ZZ(properties['cm_discriminant'])
            self._embedding_degree = ZZ(properties['embedding_degree'])
            self._j_invariant = ZZ(properties['j_invariant'])
            self._trace = ZZ(properties['trace'])
        except KeyError:
            self._j_invariant = self._ec.j_invariant()
            self._trace = self._q + 1 - self._cardinality

    def extended_ec(self, deg):
        ext_q = self._q ** deg
        ext_field = GF(ext_q, name="z", modulus=self._field['x'].irreducible_element(deg * self._field.degree()))
        if self.is_over_prime():
            return self._ec.base_extend(ext_field)
        # perhaps unnecessarily complicated coercion (str.replace :P)
        h = ext_field.gen() ** ((ext_q - 1) // (self._q - 1))
        hf = GF(self._q, name="h", modulus=h.minpoly())
        i = hf.hom([h])
        new_coeffs = list(map(lambda x: i(hf(str(x).replace(str(self._field.gen()), "h"))), self._ec.a_invariants()))
        return EllipticCurve(ext_field, new_coeffs)

    def extended_cardinality(self, deg):
        """returns curve cardinality over deg-th relative extension"""
        s_old, s_new = 2, self._trace
        for _ in range(2, deg + 1):
            s_old, s_new = s_new, self._trace * s_new - self._q * s_old
        return self._q ** deg + 1 - s_new

    def extended_trace(self, deg):
        """returns the trace of Frobenius over deg-th relative extension"""
        return self._q ** deg + 1 - self.extended_cardinality(deg)

    def extended_frobenius_disc(self, deg=1):
        """returns the Frobenius discriminant (i.e. t^2-4q) over deg-th relative extension"""
        return self.extended_trace(deg) ** 2 - 4 * self._q ** deg

    def __repr__(self):
        return f"{self._name}: {self._nbits}-bit curve in {self._form} form over {self._field_type} field"

    def __str__(self):
        return self.__repr__()

    def __lt__(self, other):
        return (self._nbits, self._name) < (other.nbits(), other.name())


def squarefree_and_factorization(x):
    """squarefree part of x and the factorization of x or 'NO DATA (timed out)'"""
    fct = timeout(factor, [x], timeout_duration=20)
    if isinstance(fct, str):
        return fct
    n = 1
    for p, e in fct:
        if e % 2:
            n *= p
    return n * fct.unit(), fct
