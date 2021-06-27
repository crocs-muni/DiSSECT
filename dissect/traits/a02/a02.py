from sage.all import ZZ, sqrt

from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve


def a02_curve_function(curve: CustomCurve):
    """
    Computation of d_K (cm_disc), v (max_conductor) and factorization of D where D=t^2-4q = v^2*d_K
    Returns a dictionary (keys: 'cm_disc', 'factorization', 'max_conductor')
    """
    curve_result = {"cm_disc": None, "factorization": None, "max_conductor": None}
    frob_disc = curve.extended_frobenius_disc()
    frob_disc_factor = curve.frobenius_disc_factorization()
    if isinstance(frob_disc_factor, str):
        return curve_result
    if curve.cm_discriminant() is None:
        return {"cm_disc": None, "factorization": None, "max_conductor": None}
    return {"cm_disc": curve.cm_discriminant(), "factorization": [f for f, e in frob_disc_factor for _ in range(e)],
            "max_conductor": ZZ(sqrt(frob_disc // curve.cm_discriminant()))}


def compute_a02_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "a02", a02_curve_function, desc=desc, verbose=verbose)
