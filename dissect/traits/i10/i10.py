from pathlib import Path

from sage.all import ZZ

from dissect.definitions import EFD_PATH
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve
from dissect.utils.zvp.gen_zvp import ZVPFinder


def i10_curve_function(curve: CustomCurve, multiple, formula_file):
    """Computes the roots given by ZVP conditions"""
    q = curve.q()
    _, _, _, a, b = curve.ec().ainvs()
    formula_path = Path(EFD_PATH, formula_file)
    ZVP = ZVPFinder(formula_path, multiple)
    points = []
    for point in ZVP.find_points(ZZ(a), ZZ(b), q):
        points.append([ZZ(point[0]), ZZ(point[1])])
    curve_results = {"points": points, "len": len(points)}
    return curve_results


def compute_i10_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "i10", i10_curve_function, desc=desc, verbose=verbose)
