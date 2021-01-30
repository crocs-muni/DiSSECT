#!/usr/bin/env python3
from pathlib import Path

from sage.all import ZZ

from curve_analyzer.definitions import EFD_PATH
from curve_analyzer.traits.trait_interface import compute_results
from curve_analyzer.utils.zvp.gen_zvp import ZVPFinder


def i11_curve_function(curve, formula_file):
    """Computes the roots given by ZVP conditions that depend on one point only"""
    q = curve.q
    _, _, _, a, b = curve.EC.ainvs()
    formula_path = Path(EFD_PATH, formula_file)
    ZVP = ZVPFinder(formula_path, multiple=1, one_point_dependent=True)
    points = []
    for point in ZVP.find_points(ZZ(a), ZZ(b), q):
        points.append([ZZ(point[0]), ZZ(point[1])])
    curve_results = {"points": points, "len": len(points)}
    return curve_results


def compute_i11_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'i11', i11_curve_function, desc=desc, verbose=verbose)
