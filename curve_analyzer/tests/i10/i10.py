from pathlib import Path

from curve_analyzer.definitions import ZVP_PATH
from curve_analyzer.tests.test_interface import compute_results
from curve_analyzer.utils.zvp.gen_zvp import ZVPFinder


def i10_curve_function(curve, multiple, formula_file):
    """Computes the roots given by ZVP conditions"""
    q = curve.q
    _, _, _, a, b = curve.EC.ainvs()
    formula_path = Path(ZVP_PATH, formula_file)
    ZVP = ZVPFinder(formula_path, multiple)
    roots = ZVP.find_zvp_roots(a, b, q)
    curve_results = {"roots": roots, "len": len(roots)}
    return curve_results


def compute_i10_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'i10', i10_curve_function, desc=desc, verbose=verbose)
