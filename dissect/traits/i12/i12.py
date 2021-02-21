#!/usr/bin/env python3
import io
from contextlib import redirect_stdout
from pathlib import Path

from sage.all import load, GF

from dissect.definitions import UNROLLED_ADDITION_FORMULAE_PATH
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve


def i12_curve_function(curve: CustomCurve, unrolled_formula_file):
    """Tries to compute the variety of exceptional points where the unrolled_formula fails"""

    q = curve.q
    K = GF(q)
    curve_results = {"ideal": None, "dimension": None, "variety": None}

    if curve.form == "Weierstrass":
        if "shortw" not in unrolled_formula_file:
            return curve_results
        shortw_a, shortw_b = curve.EC.a4(), curve.EC.a6()
        if ("jacobian_0_" in unrolled_formula_file and K(shortw_a) != K(0)) \
                or ("w12_0_" in unrolled_formula_file and K(shortw_b) != K(0)) \
                or ("_1_" in unrolled_formula_file and K(shortw_a) != K(-1)) \
                or ("_3_" in unrolled_formula_file and K(shortw_a) != K(-3)):
            return curve_results

    elif curve.form == "TwistedEdwards":
        if "twisted" not in unrolled_formula_file:
            return curve_results
        twisted_a = curve.params['a']['raw']
        twisted_d = curve.params['d']['raw']
        if "extended_1_" in unrolled_formula_file and K(twisted_a) != K(-1):
            return curve_results

    elif curve.form == "Edwards":
        if "edwards" not in unrolled_formula_file:
            return curve_results
        edwards_c = curve.params['c']['raw']
        edwards_d = curve.params['d']['raw']

    else:
        return curve_results

    # get all output polynomials
    unrolled_formula = Path(UNROLLED_ADDITION_FORMULAE_PATH, unrolled_formula_file)
    load(unrolled_formula)
    output_polys = [X3, Y3, Z3]  # the other output polynomials such as T3, ZZ3, ZZZ3 are not needed for our purposes

    # clean up the ring and convert the output polynomials
    gen1, gen2 = pr.gens()[:2]
    pr_clean = pr.remove_var(gen1).remove_var(gen2).change_ring(K)

    if curve.form == "Weierstrass":
        output_polys_converted = [pr_clean(pr(poly)(a=shortw_a, b=shortw_b)) for poly in output_polys]
        I = pr_clean.ideal(Y1 ** 2 - X1 ** 3 - shortw_a * X1 - shortw_b,
                           Y2 ** 2 - X2 ** 3 - shortw_a * X2 - shortw_b,
                           *output_polys_converted)

    elif curve.form == "TwistedEdwards":
        output_polys_converted = [pr_clean(pr(poly)(a=twisted_a, d=twisted_d)) for poly in output_polys]
        I = pr_clean.ideal(twisted_a * X1 ** 2 + Y1 ** 2 - (1 + twisted_d * X1 ** 2 * Y1 ** 2),
                           twisted_a * X2 ** 2 + Y2 ** 2 - (1 + twisted_d * X2 ** 2 * Y2 ** 2),
                           *output_polys_converted)

    elif curve.form == "Edwards":
        output_polys_converted = [pr_clean(pr(poly)(c=edwards_c, d=edwards_d)) for poly in output_polys]
        I = pr_clean.ideal(X1 ** 2 + Y1 ** 2 - edwards_c * (1 + edwards_d * X1 ** 2 * Y1 ** 2),
                           X2 ** 2 + Y2 ** 2 - edwards_c * (1 + edwards_d * X2 ** 2 * Y2 ** 2),
                           *output_polys_converted)

    # do the actual computation
    with redirect_stdout(io.StringIO()):
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
