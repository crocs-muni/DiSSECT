#!/usr/bin/env python3
from sage.all import ZZ, ecm, factor, Integers, sqrt, PolynomialRing
from sage.rings.finite_rings.all import GF

from dissect.traits.trait_interface import timeout
from dissect.utils.custom_curve import CustomCurve


def is_torsion_cyclic(curve: CustomCurve, prime, deg, iterations=20):
    """
    True if the l-torsion is cyclic and False otherwise (bicyclic). Note that this is probabilistic only.
    """
    card = curve.extended_cardinality(deg)
    m = ZZ(card / prime)
    ext_ec = curve.extended_ec(deg)
    for _ in range(iterations):
        point = ext_ec.random_element()
        if not (m * point == ext_ec(0)):
            return True
    return False


def embedding_degree_q(q, prime):
    """returns the l-embedding degree with respect to q"""
    return (Integers(prime)(q)).multiplicative_order()


def factorization(x, timeout_duration=20, use_ecm=True):
    """Returns the factorization of abs(x) as a list or 'NO DATA (timed out)'"""
    if use_ecm:
        return timeout(ecm.factor, [abs(x)], timeout_duration=timeout_duration)
    else:
        result = timeout(factor, [abs(x)], timeout_duration=timeout_duration)
        if not isinstance(result, str):
            result = [i[0] for i in list(result) for _ in range(i[1])]
        return result


def squarefree_part(x, timeout_duration=20, use_ecm=True):
    """return the squarefree part of x or 'NO DATA (timed out)'"""
    sf = squarefree_and_factorization(x=x, timeout_duration=timeout_duration, use_ecm=use_ecm)
    if isinstance(sf, str):
        return sf
    else:
        return sf[0]


def squarefree_and_factorization(x, timeout_duration=20, use_ecm=True):
    """return the (squarefree part of x and the factorization of abs(x)) or 'NO DATA (timed out)'"""
    f = factorization(x, timeout_duration=timeout_duration, use_ecm=use_ecm)
    if isinstance(f, str):
        return f
    else:
        squarefree = 1
        for p in set(f):
            if f.count(p) % 2 == 1:
                squarefree *= p
        if x < 0:
            sign = -1
        else:
            sign = 1
        return sign * squarefree, f


def square_part(x, timeout_duration=20, use_ecm=True):
    """return the square part of x or 'NO DATA (timed out)'"""
    squarefree = squarefree_part(
        x=x, timeout_duration=timeout_duration, use_ecm=use_ecm
    )
    if isinstance(squarefree, str):
        return squarefree
    else:
        return ZZ(x // squarefree)


def square_part_square_root(x, timeout_duration=20, use_ecm=True):
    """return the square root of square part of x or 'NO DATA (timed out)'"""
    square = square_part(x=x, timeout_duration=timeout_duration, use_ecm=use_ecm)
    if isinstance(square, str):
        return square
    else:
        return sqrt(square)


def eigenvalues(curve: CustomCurve, prime, s=1):
    """Computes the eigenvalues of Frobenius endomorphism in F_l, or in F_(l^2) if s=2"""
    x = PolynomialRing(GF(prime ** s), "x").gen()
    q = curve.q()
    t = curve.trace()
    f = x ** 2 - t * x + q
    return f.roots()


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
