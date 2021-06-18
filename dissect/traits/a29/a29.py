from sage.all import ZZ, QQ, sqrt, EllipticCurve

from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve

def a29_curve_function(curve: CustomCurve):
    """
    Computation of the torsion order of E' where E' is the lift of the givne
    curve to Q. By lift, we mean lift of coefficients to ZZ
    """

    a,b = ZZ(curve.params['a']['raw']),ZZ(curve.params['b']['raw'])
    E = EllipticCurve(QQ,[a,b])
    return {'Q_torsion':E.torsion_order()}


def compute_a29_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "a29", a29_curve_function, desc=desc, verbose=verbose)
