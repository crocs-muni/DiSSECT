from sage.all import EllipticCurve, ZZ, GF, factor  # import sage library


# Converting functions using formulas in https://tools.ietf.org/id/draft-struik-lwip-curve-representations-00.html


def montgomery_to_short_weierstrass(F, A, B, x, y):
    a = F((3 - A ** 2) / (3 * B ** 2))
    b = F((2 * A ** 3 - 9 * A) / (27 * B ** 3))
    if x == "" or y == "" or x is None or y is None:
        return a, b, None, None
    else:
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

    if u == "" or v == "" or u is None or v is None:
        if scaling:
            return A, 1, None, None
        else:
            return A, B, None, None
    else:
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


def get_poly(poly_dict, K):
    w = K.gens()[0]
    poly = 0
    for mono in poly_dict:
        poly += ZZ(mono["coeff"]) * w ** ZZ(mono["power"])
    return K(poly)


class CustomCurve:
    """Class for unified representation of curves from databases"""

    def __init__(self, db_curve):
        """the "fixed" part of attributes"""
        self.name = db_curve["name"]
        self.order = ZZ(db_curve["order"])
        self.source = db_curve["category"]
        self.field_desc = db_curve["field"]
        self.form = db_curve["form"]
        self.params = db_curve["params"]
        self.desc = db_curve["desc"]
        self.cofactor = ZZ(db_curve["cofactor"])
        self.cardinality = self.order * self.cofactor
        self.nbits = self.order.nbits()
        self.generator_desc = db_curve["generator"]
        self.field = None
        self.EC = None
        self.generator = None
        self.q = None
        self.trace = None
        """the "variable" part of attributes"""
        try:
            self.seed = db_curve["seed"]
        except KeyError:
            self.seed = None
        try:
            self.x = ZZ(db_curve["generator"]["x"]["raw"])
            self.y = ZZ(db_curve["generator"]["y"]["raw"])
        except (TypeError, KeyError):
            self.x = None
            self.y = None
        self.set()

    def get_xy(self, extension=False):
        if self.generator_desc is None:
            return None, None
        if extension:
            x = get_poly(self.generator_desc["x"]["poly"], self.field)
            y = get_poly(self.generator_desc["y"]["poly"], self.field)
        else:
            x = self.generator_desc["x"]["raw"]
            y = self.generator_desc["y"]["raw"]
            try:
                x = ZZ(x)
                y = ZZ(y)
            except TypeError:
                pass
        return x, y

    def set_generator(self, binary=False, extension=False, x=None, y=None):
        if x is None or y is None:
            x, y = self.get_xy(extension)
        if x is None or y is None or x == "" or y == "":
            self.generator = None
        else:
            if binary:
                self.generator = self.EC(
                    self.field.fetch_int(x), self.field.fetch_int(y)
                )
            else:
                self.generator = self.EC(x, y)

    def set(self):
        if self.form == "Weierstrass":
            if self.field_desc["type"] == "Prime":
                p = ZZ(self.field_desc["p"])
                F = GF(p, proof=False)
                a = ZZ(self.params["a"]["raw"])
                b = ZZ(self.params["b"]["raw"])
                self.EC = EllipticCurve(F, [a, b])
                self.set_generator()

            elif self.field_desc["type"] == "Binary":
                degree = ZZ(self.field_desc["degree"])
                F = GF(2)["w"]
                modulus = get_poly(self.field_desc["poly"], F)
                K = GF(2 ** degree, "w", modulus, proof=False)
                a = ZZ(self.params["a"]["raw"])
                b = ZZ(self.params["b"]["raw"])
                self.EC = EllipticCurve(
                    K, [1, K.fetch_int(ZZ(a)), 0, 0, K.fetch_int(ZZ(b))]
                )  # xy, x^2, y, x, 1
                self.field = K
                self.set_generator(binary=True)

            elif self.field_desc["type"] == "Extension":
                base = ZZ(self.field_desc["base"])
                degree = ZZ(self.field_desc["degree"])
                F = GF(base, proof=False)["w"]
                modulus = get_poly(self.field_desc["poly"], F)
                K = GF(base ** degree, "w", modulus, proof=False)
                a = get_poly(self.params["a"]["poly"], K)
                b = get_poly(self.params["b"]["poly"], K)
                self.EC = EllipticCurve(K, [a, b])
                self.set_generator(extension=True)

        elif self.form == "Montgomery":
            assert self.field_desc["type"] != "Extension"  # TO DO
            A = ZZ(self.params["a"]["raw"])
            B = ZZ(self.params["b"]["raw"])
            p = ZZ(self.field_desc["p"])
            F = GF(p, proof=False)
            x, y = self.get_xy()
            a, b, u, v = montgomery_to_short_weierstrass(F, A, B, x, y)
            self.EC = EllipticCurve(F, [a, b])
            self.set_generator(x=u, y=v)

        elif self.form in ["Edwards", "TwistedEdwards"]:
            # we assume c=1
            assert self.field_desc["type"] != "Extension"  # TO DO
            if self.form == "Edwards":
                aa = 1
            else:
                # TwistedEdwards case
                aa = ZZ(self.params["a"]["raw"])
            d = ZZ(self.params["d"]["raw"])
            p = ZZ(self.field_desc["p"])
            F = GF(p, proof=False)
            x, y = self.get_xy()
            a, b, xx, yy = twisted_edwards_to_short_weierstrass(F, aa, d, x, y)
            self.EC = EllipticCurve(F, [a, b])
            self.set_generator(x=xx, y=yy)
        else:
            self.EC = "Not implemented"

        self.field = self.EC.base_field()
        self.q = self.field.order()
        self.EC.set_order(self.cardinality, num_checks=0)
        self.trace = self.q + 1 - self.cardinality

    def __repr__(self):
        return (
            self.name
            + ": "
            + str(self.nbits)
            + "-bit curve in "
            + self.form
            + " form over "
            + self.field_desc["type"]
            + " field"
        )

    def __str__(self):
        return self.__repr__()

    def __lt__(self, other):
        return (self.order.nbits(), self.name) < (other.order.nbits(), other.name)


def customize_curve(curve):
    db_curve = {}
    db_curve["name"] = "joe"
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
    return CustomCurve(db_curve)
