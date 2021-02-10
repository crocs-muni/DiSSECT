#!/usr/bin/env python3
from sage.all import ZZ, EllipticCurve, ecm, factor
from sage.functions.log import log
from sage.rings.finite_rings.all import GF

from dissect.traits.trait_interface import timeout
from dissect.utils.custom_curve import CustomCurve


def ext_card(curve: CustomCurve, deg, sage=False):
    """returns curve cardinality over deg-th relative extension"""
    if sage:
        return curve.EC.cardinality(extension_degree=deg)
    tr = curve.trace
    q = curve.q
    s_old, s_new = 2, tr
    for _ in range(2, deg + 1):
        s_old, s_new = s_new, tr * s_new - q * s_old
    card_high = q ** deg + 1 - s_new
    return card_high


def ext_trace(curve: CustomCurve, deg):
    """returns the trace of Frobenius over deg-th relative extension"""
    return curve.q ** deg + 1 - ext_card(curve, deg)


def ext_disc(curve: CustomCurve, deg=1):
    """returns the CM discriminant (up to a square) over deg-th relative extension"""
    q = curve.q
    card_ext = ext_card(curve, deg)
    ext_tr = q ** deg + 1 - card_ext
    return ext_tr ** 2 - 4 * q ** deg


def stupid_coerce_K_to_L(element, K, L):
    """returns the element of K as an element of L"""
    name_K = str(K.gen())
    name_L = str(L.gen())
    return L(str(element).replace(name_K, name_L))


def extend(curve: CustomCurve, deg):
    """returns curve over the deg-th relative extension"""
    E = curve.EC
    q = curve.q
    K = curve.field
    if q % 2 != 0:
        R = K['x']
        pol = R.irreducible_element(deg)
        Fext = GF(q ** deg, name='z', modulus=pol)
        return E.base_extend(Fext)
    charac = K.characteristic()
    R = GF(charac)['x']
    ext_deg = q ** deg
    pol = R.irreducible_element(deg * ZZ(log(q, charac)))
    Kext = GF(ext_deg, name='ex', modulus=pol)
    gKext = Kext.gen()

    h = gKext ** ((ext_deg - 1) // (q - 1))
    assert charac ** (h.minpoly().degree()) == q
    H = GF(q, name='h', modulus=h.minpoly())
    inclusion = H.hom([h])

    new_coefficients = [inclusion(stupid_coerce_K_to_L(a, K, H)) for a in E.a_invariants()]
    EE = EllipticCurve(Kext, new_coefficients)
    return EE


def is_torsion_cyclic(curve: CustomCurve, l, deg, iterations=20):
    """
    True if the l-torsion is cyclic and False otherwise (bicyclic). Note that this is probabilistic only.
    """
    card = ext_card(curve, deg)
    m = ZZ(card / l)
    EE = extend(curve, deg)
    for _ in range(iterations):
        P = EE.random_element()
        if not (m * P == EE(0)):
            return True
    return False


def factorization(x, timeout_duration=20, use_ecm=True):
    """return the factorization of abs(x) as a list or 'NO DATA (timed out)'"""
    if use_ecm:
        return timeout(ecm.factor, [abs(x)], timeout_duration=timeout_duration)
    else:
        return [i[0] for i in list(factor(abs(x))) for _ in range(i[1])]


def squarefree_part(x, timeout_duration=20, use_ecm=True):
    """return the squarefree part of x or 'NO DATA (timed out)'"""
    F = squarefree_and_factorization(x=x, timeout_duration=timeout_duration, use_ecm=use_ecm)
    if F == 'NO DATA (timed out)':
        return F
    else:
        return F[0]


def squarefree_and_factorization(x, timeout_duration=20, use_ecm=True):
    """return the (squarefree part of x and the factorization of abs(x)) or 'NO DATA (timed out)'"""
    F = factorization(x, timeout_duration=timeout_duration, use_ecm=use_ecm)
    if F == 'NO DATA (timed out)':
        return F
    else:
        squarefree = 1
        for p in set(F):
            if F.count(p) % 2 == 1:
                squarefree *= p
        if x < 0:
            sign = -1
        else:
            sign = 1
        return (sign * squarefree, F)
