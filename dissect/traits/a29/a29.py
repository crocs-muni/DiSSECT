from sage.all import ZZ, QQ, EllipticCurve

from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve


def a29_curve_function(curve: CustomCurve):
    """
    Computation of the torsion order of E' where E' is the lift of the given
    curve to Q. By lift, we mean lift of coefficients to ZZ
    """
    try:
        a, b = ZZ(curve.a()), ZZ(curve.b())
    except TypeError:
        a, b = ZZ(curve.params()['a']['raw']), ZZ(curve.params()['b']['raw'])
    except ValueError:
        return {'Q_torsion':None}
    ec = EllipticCurve(QQ, [a, b])
    return {'Q_torsion': ec.torsion_order()}


def compute_a29_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "a29", a29_curve_function, desc=desc, verbose=verbose)
