from dissect.utils.curve_handler import import_curve_db
from dissect.utils.custom_curve import CustomCurve
from sage.all import ZZ, GF, PolynomialRing, Integers


def test_point(curve, p):
    x, y = PolynomialRing(GF(p), name=['x', 'y'])
    if curve['form'] == 'Weierstrass':
        a, b = unpack(curve['params']['a']), unpack(curve['params']['b'])
        gx, gy = unpack(curve['generator']['x']), unpack(curve['generator']['y'])
        poly = y ** 2 - x ** 3 - a * x - b
    if curve['form'] == 'Montgomery':
        a, b = unpack(curve['params']['a']), unpack(curve['params']['b'])
        gx, gy = unpack(curve['generator']['x']), unpack(curve['generator']['y'])
        poly = b * y ** 2 - x ** 3 - a * x ** 2 - x

    if curve['form'] == 'Edwards':
        c, d = unpack(curve['params']['c']), unpack(curve['params']['d'])
        gx, gy = unpack(curve['generator']['x']), unpack(curve['generator']['y'])
        poly = y ** 2 + x ** 2 - c ** 2 * (1 + d * x ** 2 * y ** 2)

    if curve['form'] == 'TwistedEdwards':
        a, d = unpack(curve['params']['a']), unpack(curve['params']['d'])
        gx, gy = unpack(curve['generator']['x']), unpack(curve['generator']['y'])
        poly = a * x ** 2 + y ** 2 - 1 - d * x ** 2 * y ** 2

    assert poly(gx, gy) == 0, "generator is not on the curve"


def test_discriminant(ec, discriminant):
    assert ec.discriminant() == discriminant, "discriminant"


def test_jinvariant(ec, j):
    assert ec.j_invariant() == j, 'j-invariant'


def test_trace_of_frobenius(trace, q, cardinality):
    assert q + 1 - trace == cardinality, 'trace'


def test_embedding_degree(order, q, edeg):
    assert (Integers(order)(q)).multiplicative_order() == edeg, 'embedding degree'


def test_anomalous(cardinality, p, anomalous):
    assert (cardinality % p == 0) == anomalous, 'anomalous'


def test_supersingular(trace, p, supersing):
    assert (trace % p == 0) == supersing, 'supersingular'


def test_cm_disc(trace, q, cm):
    disc = trace ** 2 - 4 * q
    d = disc.squarefree_part()
    if d % 4 != 1:
        d *= 4
    assert cm == d, 'cm disc'


# TODO
def test_conductor():
    pass


# TODO
def test_torsion_degrees():
    pass


def unpack(value):
    return ZZ(value['raw'])


# TODO extensions, binary
def test_curve(curve, source):
    try:
        assert curve['category'].lower() == source.lower(), "source"
        p = ZZ(curve['field']['p'])
        field = GF(p)
        assert p.nbits() == curve['field']['bits'], 'prime bits'
        characteristics = curve['characteristics']
        order, cofactor = ZZ(curve['order']), ZZ(curve['cofactor'])
        cardinality = order * cofactor
        test_trace_of_frobenius(ZZ(characteristics['trace_of_frobenius']), p, cardinality)
        test_anomalous(cardinality, p, characteristics['anomalous'])
        test_embedding_degree(order, p, ZZ(characteristics['embedding_degree']))
        cc = CustomCurve(curve)
        test_discriminant(cc.EC, field(characteristics['discriminant']))
        test_jinvariant(cc.EC, field(characteristics['j_invariant']))
    except KeyError:
        pass
    except AssertionError as e:
        print(source, curve['name'], e)


def main():
    curve_db = import_curve_db()
    for source, db in curve_db.items():
        curves = db['curves']
        for curve in curves:
            if curve['field']['type'] != "Prime":
                continue
            test_curve(curve, source)


if __name__ == '__main__':
    main()
