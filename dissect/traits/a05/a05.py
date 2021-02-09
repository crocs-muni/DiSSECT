from sage.all import ZZ, PolynomialRing, GF, Integers

from dissect.traits.trait_interface import compute_results
from dissect.traits.trait_utils import ext_card, is_torsion_cyclic
from dissect.utils.custom_curve import CustomCurve


def embedding_degree_q(q, l):
    """returns embedding degree with respect to q"""
    return (Integers(l)(q)).multiplicative_order()


def find_least_torsion(q, order, l):
    """
    Computes the smallest extension which contains a nontrivial l-torsion point
    Returns the degree
    """
    x = PolynomialRing(GF(l ** 2), 'x').gen()
    t = q + 1 - order

    f = x ** 2 - t * x + q

    roots = [r[0] for r in f.roots() for _ in range(r[1])]

    return min(roots[0].multiplicative_order(), roots[1].multiplicative_order())


def find_full_torsion(E, q, order, l, least, field):
    """
    Computes the smallest extension which contains full l-torsion subgroup
    Least is the result of find_least_torsion
    Returns the degree
    """
    q_least = q ** least
    k = embedding_degree_q(q_least, l)
    # k satisfies l|a^k-1 where a,1 are eigenvalues of Frobenius of extended E
    if k > 1:  # i.e. a!=1
        return k * least
    else:  # i.e. a==1, we have two options for the geometric multiplicity
        card = ext_card(q, order, least)
        if (card % l ** 2) == 0 and not is_torsion_cyclic(E, q, order, l, least, field):  # geom. multiplicity is 2
            return least
        else:  # geom. multiplicity is 1
            return l * least


def find_torsions(E, q, order, l, field):
    """Returns a triple of extensions containing torsion"""
    least = find_least_torsion(q, order, l)
    if least == l ** 2 - 1:
        full = least

    else:
        full = find_full_torsion(E, q, order, l, least, field)

    return least, full, ZZ(full / least)


def a05_curve_function(curve: CustomCurve, l):
    """Computes find_torsions for given l and returns a dictionary"""
    E = curve.EC
    q = curve.q
    order = curve.order * curve.cofactor
    curve_results = {}

    try:
        least, full, relative = find_torsions(E, q, order, l, curve.field)

    except (ArithmeticError, TypeError, ValueError) as _:
        least, full, relative = None, None, None

    curve_results['least'] = least
    curve_results['full'] = full
    curve_results['relative'] = relative

    return curve_results


def compute_a05_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a05', a05_curve_function, desc=desc, verbose=verbose)
