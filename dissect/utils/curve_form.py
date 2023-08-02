from sage.all import ZZ


# Converting class using formulas in https://tools.ietf.org/id/draft-struik-lwip-curve-representations-00.html

class CurveForm:
    def __init__(self, field, curve):
        self._field = field
        self._form = curve['form']
        self._a, self._b, self._ma, self._mb, self._ea, self._ed = [None] * 6
        if self._form == "Weierstrass":
            self._a, self._b = self.field_conversion(curve['a'], curve['b'])
        elif self._form == "Montgomery":
            self._ma, self._mb = self.field_conversion(curve['a'], curve['b'])
            self.montgomery_to_weierstrass()
        else:
            self._ea, self._ed = self.field_conversion(curve['a'], curve['d'])
            self._edwards_scaling = 1
            self.twisted_edwards_to_montgomery()
            self.montgomery_to_weierstrass()

    def field(self):
        return self._field

    def form(self):
        return self._form

    def field_conversion(self, m, n):
        if self._field.is_prime_field():
            return ZZ(m["raw"]), ZZ(n["raw"])
        if self._field.characteristic() == 2:
            return self._field.from_integer(ZZ(m["raw"])), self._field.from_integer(ZZ(n["raw"]))
        return dict_to_poly(m["poly"], self.field()), dict_to_poly(n["poly"], self.field())

    def a(self):
        return self._a

    def b(self):
        return self._b

    def point(self, x, y):
        x, y = self.field_conversion(x, y)
        if self._form == "Weierstrass":
            return x, y
        if self._form == "Montgomery":
            return self.montgomery_to_weierstrass_point(x, y)
        return self.twisted_edwards_to_weierstrass_point(x, y)

    def montgomery_to_weierstrass(self):
        self._a = self._field((3 - self._ma ** 2) / (3 * self._mb ** 2))
        self._b = self._field((2 * self._ma ** 3 - 9 * self._ma) / (27 * self._mb ** 3))

    def twisted_edwards_to_montgomery(self):
        self._ma = self._field((2 * self._ea + 2 * self._ed) / (self._ea - self._ed))
        self._mb = self._field(4 / (self._ea - self._ed))
        if self._field(self._mb).is_square():
            self._edwards_scaling = self._field(1 / self._mb).sqrt()
            self._mb = 1

    def montgomery_to_weierstrass_point(self, x, y):
        u = self._field((3 * x + self._ma) / (3 * self._mb))
        v = self._field(y / self._mb)
        return u, v

    def twisted_edwards_to_montgomery_point(self, u, v):
        x = self._field((1 + v) / (1 - v))
        y = self._field((1 + v) / ((1 - v) * u)) / self._edwards_scaling
        return x, y

    def twisted_edwards_to_weierstrass_point(self, x, y):
        x, y = self.twisted_edwards_to_montgomery_point(x, y)
        return self.montgomery_to_weierstrass_point(x, y)


def dict_to_poly(poly_dict, field):
    w = field.gens()[0]
    poly = 0
    for mono in poly_dict:
        poly += ZZ(mono["coeff"]) * w ** ZZ(mono["power"])
    return field(poly)
