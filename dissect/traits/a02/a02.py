from sage.all import ZZ, sqrt, squarefree_part

from dissect.traits.trait_interface import compute_results
import dissect.traits.trait_utils as tu
from dissect.traits.trait_utils import ext_cm_disc
from dissect.utils.custom_curve import CustomCurve


def a02_curve_function(curve: CustomCurve):
    """
    Computation of d_K (cm_disc), v (max_conductor) and factorization of D where D=t^2-4q = v^2*d_K
    Returns a dictionary (keys: 'cm_disc', 'factorization', 'max_conductor')
    """
    D = ext_cm_disc(curve, deg=1)
    d = squarefree_part(D)
    disc = d
    if d % 4 != 1:
        disc *= 4
    curve_results = {}
    curve_results['cm_disc'] = disc
    factorization = tu.factorization(D)
    if factorization == 'NO DATA (timed out)':
        curve_results['factorization'] = []
    else:
        tuples_to_lists = [list(i) for i in list(factorization)]
        curve_results['factorization'] = tuples_to_lists
    curve_results['max_conductor'] = ZZ(sqrt(D / disc))
    return curve_results


def compute_a02_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a02', a02_curve_function, desc=desc, verbose=verbose)
