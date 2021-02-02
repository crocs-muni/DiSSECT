#!/usr/bin/env python3
from pathlib import Path

from sage.all import PolynomialRing, GF

from curve_analyzer.definitions import EFD_PATH
from curve_analyzer.traits.trait_interface import compute_results
from curve_analyzer.utils.zvp.gen_zvp import ZVPFinder


def i12_curve_function(curve, formula_file):
    """Tries to compute the variety of exceptional points where the formula fails"""
    q = curve.q
    _, _, _, a, b = curve.EC.ainvs()
    formula_path = Path(EFD_PATH, formula_file)
    ZVP = ZVPFinder(formula_path, multiple=1)
    R = PolynomialRing(GF(q), ('x1', 'x2', 'y1', 'y2'))
    x1, x2, y1, y2 = R.gens()
    X3, Y3, Z3 = [poly(a=a, b=b) for poly in ZVP.output_polys]
    I = R.ideal(y1 ** 2 - x1 ** 3 - a * x1 - b, y2 ** 2 - x2 ** 3 - a * x2 - b, X3, Y3, Z3)
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
