from sage.all import PolynomialRing, ClassicalModularPolynomialDatabase
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve


def a28_curve_function(curve: CustomCurve, l):
    """
    Computes number of j-invariants j2 such that Phi_l(j,j2) where Phi_l is the l-modular polynomial.
    """
    Phi = ClassicalModularPolynomialDatabase()[l]
    x = PolynomialRing(curve.field(), "x").gen()
    j = curve.j_invariant()
    f = Phi(j, x)
    return {"len": sum([i[1] for i in f.roots()])}


def compute_a28_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "a28", a28_curve_function, desc=desc, verbose=verbose)
