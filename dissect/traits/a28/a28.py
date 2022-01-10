from sage.all import PolynomialRing
from dissect.utils.kohel.modular_polynomials import modular_polynomials
from dissect.utils.custom_curve import CustomCurve


def a28_curve_function(curve: CustomCurve, l):
    """
    Computes number of j-invariants j2 such that Phi_l(j,j2) where Phi_l is the l-modular polynomial.
    """
    Phi = modular_polynomials(l)
    x = PolynomialRing(curve.field(), "x").gen()
    j = curve.j_invariant()
    f = Phi(j, x)
    return {"len": sum([i[1] for i in f.roots()])}
