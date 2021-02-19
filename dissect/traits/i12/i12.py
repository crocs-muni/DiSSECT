#!/usr/bin/env python3
from pathlib import Path

from sage.all import load, GF

from dissect.definitions import UNROLLED_ADDITION_FORMULAE_PATH
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve


def i12_curve_function(curve: CustomCurve, unrolled_formula_file):
    """Tries to compute the variety of exceptional points where the unrolled_formula fails"""

    q = curve.q
    K = GF(q)
    _, _, _, aa, bb = curve.EC.ainvs()
    curve_results = {"ideal": None, "dimension": None, "variety": None}
    if ('shortw' not in unrolled_formula_file)\
            or ("_0_" in unrolled_formula_file and K(aa) != K(0)) \
            or ("_1_" in unrolled_formula_file and K(aa) != K(-1)) \
            or ("_3_" in unrolled_formula_file and K(aa) != K(-3)):
        return curve_results

    # get all output polynomials
    unrolled_formula = Path(UNROLLED_ADDITION_FORMULAE_PATH, unrolled_formula_file)
    load(unrolled_formula)
    output_polys = [X3, Y3, Z3]  # the other output polynomials such as T3, ZZ3, ZZZ3 are not needed for our purposes

    # clean up the ring and convert the output polynomials
    a, b = pr.gens()[:2]
    pr_clean = pr.remove_var(a).remove_var(b).change_ring(K)
    output_polys_converted = [pr_clean(pr(poly)(a=aa, b=bb)) for poly in output_polys]
    I = pr_clean.ideal(Y1 ** 2 - X1 ** 3 - aa * X1 - bb, Y2 ** 2 - X2 ** 3 - aa * X2 - bb, *output_polys_converted)

    # do the actual computation
    try:
        variety = I.variety()
    except (ValueError, NotImplementedError):
        variety = None
    try:
        dimension = I.dimension()
    except NotImplementedError:
        dimension = None
    curve_results = {"ideal": I, "dimension": dimension, "variety": variety}
    return curve_results


def compute_i12_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'i12', i12_curve_function, desc=desc, verbose=verbose)
