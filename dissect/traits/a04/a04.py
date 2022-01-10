from dissect.utils.utils import Factorization
from dissect.utils.custom_curve import CustomCurve

TRAIT_TIMEOUT = 30


def near_order_factorizations(n, sign="+", k=10, t=10):
    """Computer factorization of k*n+1 (k*n-1) if 'sign' is "+" ("-") in time 't' """
    assert sign in ["+", "-"]

    if sign == "+":
        m = k * n + 1
    else:
        m = k * n - 1
    return Factorization(m, timeout_duration=t).factorization()


def largest_factor_bitlen(factorization):
    """Computes bit length of largest factor(last item of list) of 'factorization' """
    if isinstance(factorization, str):
        return factorization
    else:
        return factorization[-1].nbits()


def a04_curve_function(curve: CustomCurve, k):
    """
    Computes factorization of ord*k+1 and ord*k-1 and bit lengths of their largest factors
    Returns a dictionary
    """
    card = curve.cardinality()
    t = TRAIT_TIMEOUT
    curve_results = {"(+)factorization": near_order_factorizations(card, "+", k, t)}
    curve_results["(+)largest_factor_bitlen"] = largest_factor_bitlen(
        curve_results["(+)factorization"]
    )
    curve_results["(-)factorization"] = near_order_factorizations(card, "-", k, t)
    curve_results["(-)largest_factor_bitlen"] = largest_factor_bitlen(
        curve_results["(-)factorization"]
    )
    return curve_results
