#!/usr/bin/env python3
from sage.all import ZZ, EllipticCurve
from sage.functions.log import log
from sage.rings.finite_rings.all import GF

from dissect.utils.custom_curve import CustomCurve


def ext_card_curve(curve: CustomCurve, deg, sage=False):
    """returns curve cardinality over deg-th relative extension"""
    if not sage:
        return ext_card(curve.q, curve.cardinality, deg)
    else:
        return curve.EC.cardinality(extension_degree=deg)


def ext_card(q, card_low, deg):
    """returns curve cardinality over deg-th relative extension"""
    tr = q + 1 - card_low
    s_old, s_new = 2, tr
    for _ in range(2, deg + 1):
        s_old, s_new = s_new, tr * s_new - q * s_old
    card_high = q ** deg + 1 - s_new
    return card_high


def ext_trace(curve: CustomCurve, deg):
    """returns the trace of Frobenius over deg-th relative extension"""
    q = curve.q
    tr = curve.trace
    a = 2
    b = tr
    for _ in range(deg - 1):
        tmp = b
        b = tr * b - q * a
        a = tmp
    return b


def ext_cm_disc(curve: CustomCurve, deg=1):
    """returns the CM discriminant (up to a square) over deg-th relative extension"""
    q = curve.q
    card_ext = ext_card_curve(curve, deg)
    ext_tr = q ** deg + 1 - card_ext
    return ext_tr ** 2 - 4 * q ** deg


def stupid_coerce_K_to_L(element, K, L):
    name_K = str(K.gen())
    name_L = str(L.gen())
    return L(str(element).replace(name_K, name_L))


def extend(E, q, deg, field):
    """returns curve over the deg-th relative extension"""
    if q % 2 != 0:
        R = field['x']
        pol = R.irreducible_element(deg)
        Fext = GF(q ** deg, name='z', modulus=pol)
        return E.base_extend(Fext)
    K = field
    charac = K.characteristic()
    R = GF(charac)['x']
    ext_deg = q ** deg
    pol = R.irreducible_element(deg * (log(q, charac)))
    Kext = GF(ext_deg, name='ex', modulus=pol)
    gKext = Kext.gen()

    h = gKext ** ((ext_deg - 1) // (q - 1))
    assert charac ** (h.minpoly().degree()) == q
    H = GF(q, name='h', modulus=h.minpoly())
    inclusion = H.hom([h])

    new_coefficients = [inclusion(stupid_coerce_K_to_L(a, K, H)) for a in E.a_invariants()]
    EE = EllipticCurve(Kext, new_coefficients)
    return EE


def is_torsion_cyclic(E, q, order, l, deg, field, iterations=10):
    """
    True if the l-torsion is cyclic and False otherwise (bicyclic). Note that this is probabilistic only.
    """
    card = ext_card(q, order, deg)
    m = ZZ(card / l)
    EE = extend(E, q, deg, field)
    for _ in range(iterations):
        P = EE.random_element()
        if not (m * P == EE(0)):
            return True
    return False
