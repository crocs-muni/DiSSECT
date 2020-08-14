from sage.all import EllipticCurve, ZZ, GF  # import sage library


# Converting functions using formulas in https://tools.ietf.org/id/draft-struik-lwip-curve-representations-00.html


def montgomery_to_short_weierstrass(F, A, B, x, y):
    a = F((3 - A ** 2) / (3 * B ** 2))
    b = F((2 * A ** 3 - 9 * A) / (27 * B ** 3))
    u = F((3 * x + A) / (3 * B))
    v = F(y / B)
    assert (u, v) in EllipticCurve(F, [a, b])
    return a, b, u, v


def twisted_edwards_to_montgomery(F, a, d, u, v, scaling=True):
    A = F((2 * a + 2 * d) / (a - d))
    B = F(4 / (a - d))
    if not B.is_square():
        scaling = False
    s = F(1 / B).sqrt()
    x = F((1 + v) / (1 - v))
    y = F((1 + v) / ((1 - v) * u))
    if scaling:
        assert (x, y / s) in EllipticCurve(F, [0, A, 0, 1, 0])
        return A, 1, x, y / s
    return A, B, x, y


def twisted_edwards_to_short_weierstrass(F, aa, d, x, y):
    A, B, x, y = twisted_edwards_to_montgomery(F, aa, d, x, y, True)
    a, b, u, v = montgomery_to_short_weierstrass(F, A, B, x, y)
    assert (u, v) in EllipticCurve(F, [a, b])
    return a, b, u, v


# Class for unified representation of curves from databases
class CustomCurve:

    def __init__(self, db_curve):
        """the "fixed" part of attributes"""
        self.name = db_curve['name']
        self.order = ZZ(db_curve['order'])
        self.source = db_curve['category']
        self.field_desc = db_curve['field']
        self.form = db_curve['form']
        self.params = db_curve['params']
        self.desc = db_curve['desc']
        self.cofactor = ZZ(db_curve['cofactor'])
        self.cardinality = self.order * self.cofactor
        self.nbits = self.order.nbits()
        self.field = None
        self.EC = None
        self.generator = None
        self.q = None
        self.trace = None
        '''the "variable" part of attributes'''
        try:
            self.seed = db_curve['seed']
        except KeyError:
            self.seed = None
        try:
            self.x = ZZ(db_curve['generator']['x']["raw"])
            self.y = ZZ(db_curve['generator']['y']["raw"])
        except TypeError:
            self.x = None
            self.y = None
        self.set()

    def set_generator(self, coord1, coord2, binary=False):
        if self.x is None or self.y is None:
            self.generator = None
        else:
            if binary:
                self.generator = self.EC(self.field.fetch_int(coord1), self.field.fetch_int(coord2))
            else:
                self.generator = self.EC(coord1, coord2)

    def set(self):
        x = self.x
        y = self.y
        if self.form == "Weierstrass":
            a = ZZ(self.params['a']["raw"])
            b = ZZ(self.params['b']["raw"])
            if self.field_desc['type'] == "Prime":
                p = ZZ(self.field_desc['p'])
                F = GF(p)
                self.EC = EllipticCurve(F, [a, b])
                self.field = F
                self.set_generator(x, y)
            elif self.field_desc['type'] == "Binary":
                F = GF(2)['w']
                (w,) = F._first_ngens(1)
                modulus = 0
                for mono in self.field_desc["poly"]:
                    modulus += ZZ(mono["coeff"]) * w ** ZZ(mono["power"])
                m = ZZ(self.field_desc['degree'])
                K = GF(2 ** m, 'w', modulus)
                self.EC = EllipticCurve(K, [1, K.fetch_int(ZZ(a)), 0, 0, K.fetch_int(ZZ(b))])  # xy, x^2, y, x, 1
                self.generator = None
                self.field = K
                self.set_generator(x,y,True)

        elif self.form == "Montgomery":
            A = ZZ(self.params['a'])
            B = ZZ(self.params['b'])
            p = ZZ(self.field_desc['p'])
            F = GF(p)
            self.field = F
            a, b, u, v = montgomery_to_short_weierstrass(F, A, B, x, y)
            self.EC = EllipticCurve(F, [a, b])
            self.set_generator(u, v)

        elif self.form in ["Edwards", "TwistedEdwards"]:
            # we assume c=1
            if self.form == "Edwards":
                aa = 1
            if self.form == "TwistedEdwards":
                aa = ZZ(self.params['a'])
            d = ZZ(self.params['d'])
            p = ZZ(self.field_desc['p'])
            F = GF(p)
            a, b, xx, yy = twisted_edwards_to_short_weierstrass(F, aa, d, x, y)
            self.EC = EllipticCurve(F, [a, b])
            self.set_generator(xx, yy)
        else:
            self.EC = "Not implemented"

        self.q = self.EC.base_field().order()
        self.EC.set_order(self.cardinality)
        self.trace = self.q + 1 - self.cardinality

    def __repr__(self):
        return self.name + ": " + str(self.nbits) + "-bit curve in " + self.form + " form over " + self.field_desc[
            'type'] + " field"

    def __str__(self):
        return self.name + ": " + str(self.nbits) + "-bit curve in " + self.form + " form over " + self.field_desc[
            'type'] + " field"

    def __lt__(self, other):
        return (self.order, self.name) < (other.order, other.name)


# Not using for now
class SimulatedWeierstrassCurve:
    def __init__(self, F, a, b, seed):
        self.F = F
        self.nbits = self.F.order().nbits()
        self.a = F(a)
        self.b = F(b)
        self.seed = seed
        self.EC = EllipticCurve(F, [a, b])
        self.order = self.EC.order()

    def __repr__(self):
        return str(self.nbits) + "-bit Weierstrass curve"

    def __str__(self):
        return str(self.nbits) + "-bit Weierstrass curve"

    def __lt__(self, other):
        return self.order < other.order
