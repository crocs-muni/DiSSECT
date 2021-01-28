from sage.all import floor

from curve_analyzer.traits.trait_interface import compute_results

DISTANCE_32 = "distance 32"
DISTANCE_64 = "distance 64"


def i07_curve_function(curve):
    '''Computes the distance of curve order to the nearest power of 2 and to the nearest multiple of 32 and 64'''
    order = curve.order * curve.cofactor
    l = order.nbits() - 1
    u = l + 1
    L = 2 ** l
    U = 2 ** u
    distance = min(order - L, U - order)
    dist32 = min(abs(order % 32), 32 - abs(order % 32))
    dist64 = min(abs(order % 64), 64 - abs(order % 64))
    ratio = floor(order / distance)
    curve_results = {"distance": distance, "ratio": ratio, DISTANCE_32: dist32, DISTANCE_64: dist64}
    return curve_results


def compute_i07_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'i07', i07_curve_function, desc=desc, verbose=verbose)
