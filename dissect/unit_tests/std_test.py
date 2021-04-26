from dissect.utils.curve_handler import import_curve_db
from sage.all import ZZ, GF, PolynomialRing, Integers


def unpack(value, p):
    return GF(p)(ZZ(value["raw"][2:], 16))


def hex_to_int(a):
    return ZZ(a[2:], 16)


def hex_to_gf(a, p):
    return GF(p)(hex_to_int(a))


def key_catch(func):
    def func_e(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return None
        except KeyError as e:
            return e.args[0]

    return func_e


@key_catch
def test_source(curve, source):
    assert curve["category"].lower() == source.lower(), "source"


@key_catch
def test_prime_bits(curve):
    p = ZZ(curve["field"]["p"])
    assert p.nbits() == curve["field"]["bits"], "prime bits"


@key_catch
def test_point(curve):
    """Tests whether the generator lies on the curve"""
    if curve["generator"]["x"]['raw'] == "":
        return
    p = ZZ(curve["field"]["p"])
    x, y = PolynomialRing(GF(p), ['x', 'y']).gens()
    poly, gx, gy = None, None, None
    if curve["form"] == "Weierstrass":
        a, b = unpack(curve["params"]["a"], p), unpack(curve["params"]["b"], p)
        gx, gy = unpack(curve["generator"]["x"], p), unpack(curve["generator"]["y"], p)
        poly = y ** 2 - x ** 3 - a * x - b
    if curve["form"] == "Montgomery":
        a, b = unpack(curve["params"]["a"], p), unpack(curve["params"]["b"], p)
        gx, gy = unpack(curve["generator"]["x"], p), unpack(curve["generator"]["y"], p)
        poly = b * y ** 2 - x ** 3 - a * x ** 2 - x

    if curve["form"] == "Edwards":
        c, d = unpack(curve["params"]["c"], p), unpack(curve["params"]["d"], p)
        gx, gy = unpack(curve["generator"]["x"], p), unpack(curve["generator"]["y"], p)
        poly = y ** 2 + x ** 2 - c ** 2 * (1 + d * x ** 2 * y ** 2)

    if curve["form"] == "TwistedEdwards":
        a, d = unpack(curve["params"]["a"], p), unpack(curve["params"]["d"], p)
        gx, gy = unpack(curve["generator"]["x"], p), unpack(curve["generator"]["y"], p)
        poly = a * x ** 2 + y ** 2 - 1 - d * x ** 2 * y ** 2

    assert poly(gx, gy) == 0, "generator is not on the curve"


@key_catch
def test_dj(curve, p):
    disc = GF(p)(ZZ(curve['characteristics']['discriminant'], 10))
    j_invariant = GF(p)(ZZ(curve['characteristics']['j_invariant'], 10))
    if curve["form"] == "Weierstrass":
        a, b = unpack(curve["params"]["a"], p), unpack(curve["params"]["b"], p)
        assert -16 * (4 * a ** 3 + 27 * b ** 2) == disc, "discriminant"
        assert -16 * 1728 * 4 * a ** 3 / disc == j_invariant, "j-invariant"
    if curve["form"] == "Montgomery":
        pass  # TODO
    if curve["form"] == "Edwards":
        pass  # TODO
    if curve["form"] == "TwistedEdwards":
        pass  # TODO


@key_catch
def test_trace_of_frobenius(cardinality, p, curve):
    try:
        trace = ZZ(curve['characteristics']['trace_of_frobenius'], 10)
        assert p + 1 - trace == cardinality, "trace"
        return ""
    except KeyError as e:
        return e.args[0]


@key_catch
def test_embedding_degree(order, q, curve):
    edeg = ZZ(curve['characteristics']['embedding_degree'], 10)
    assert (Integers(order)(q)).multiplicative_order() == edeg, "embedding degree"


@key_catch
def test_anomalous(cardinality, p, curve):
    anomalous = curve['characteristics']['anomalous']
    assert (cardinality % p == 0) == anomalous, "anomalous"


@key_catch
def test_supersingular(cardinality, p, curve):
    supersing = curve['characteristics']['supersingular']
    assert (cardinality % p == 1) == supersing, "supersingular"


@key_catch
def test_cm_disc(cardinality, p, curve):
    cm_disc = curve['characteristics']['cm_disc']
    conductor = curve['characteristics']['conductor']
    trace = p + 1 - cardinality
    disc = trace ** 2 - 4 * p
    d = disc.squarefree_part()
    if d % 4 != 1:
        d *= 4
    assert cm_disc == d, "cm disc"
    assert conductor == ZZ((disc // d).sqrt()), "conductor"


# TODO extensions, binary
def test_curve(curve, source):
    try:
        err = set()
        err.add(test_source(curve, source))
        err.add(test_prime_bits(curve))
        err.add(test_point(curve))

        p = hex_to_int(curve['field']['p'])
        err.add(test_dj(curve,p))

        order = hex_to_int(curve['order'])
        cofactor = hex_to_int(curve['cofactor'])
        cardinality = order * cofactor
        err.add(test_trace_of_frobenius(cardinality, p, curve))
        err.add(test_embedding_degree(order, p, curve))
        err.add(test_anomalous(cardinality, p, curve))
        err.add(test_supersingular(cardinality, p, curve))

        err.add(test_cm_disc(cardinality, p, curve))
        err.remove(None)
        if err != {}:
            print("skipping",end=" ")
            for e in err:
                print(e,end=" ")

    except AssertionError as e:
        print("PROBLEM: ", e)
        return False
    return True


def test_binary(curve, source):
    try:
        test_source(curve, source)
        test_point(curve)
    except AssertionError as e:
        print(source, curve["name"], e)


def main():
    broken_curves = 0
    curve_db = import_curve_db()
    for source, db in curve_db.items():
        curves = db["curves"]
        for curve in curves:
            print(curve['name'])
            if curve["field"]["type"] == "Prime":
                broken_curves += test_curve(curve, source)
            if curve['field']['type'] == "Binary":
                # broken_curves+=test_binary(curve, source)
                pass
            print()
    print("RESULTS:")
    if broken_curves == 0:
        print("All good")
    else:
        print(broken_curves, "broken curves")


if __name__ == "__main__":
    main()
