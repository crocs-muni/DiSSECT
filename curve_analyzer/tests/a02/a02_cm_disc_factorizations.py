from sage.misc.functional import squarefree_part  # import sage library
from sage.arith.misc import factor
from sage.rings.all import Integers as ZZ
from sage.functions.other import sqrt
from curve_analyzer.tests.test_interface import pretty_print_results, compute_results


# Computation of d_K (cm_disc), v (max_conductor) and factorization of D where D=t^2-4q = v^2*d_K
# Returns a dictionary (keys: 'cm_disc', 'factorization', 'max_conductor') 
def a2_curve_function(curve):
    E = curve.EC
    t = curve.trace
    q = curve.q
    curve_results = {'cm_disc': {}, 'factorization': {}}
    D = t ** 2 - 4 * q
    d = squarefree_part(D)
    disc = d
    if d % 4 != 1:
        disc *= 4
    curve_results['cm_disc'] = disc
    curve_results['factorization'] = list(factor(D))
    curve_results['max_conductor'] = ZZ(sqrt(D / disc))
    return curve_results


def compute_a2_results(curve_list, order_bound=256, overwrite=False):
    parameters = {}
    compute_results('a2', a2_curve_function, parameters, order_bound, overwrite, curve_list=curve_list)


def pretty_print_a2_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a2', [['factorization'], ['max_conductor']],
                         ['CM disc factorization', 'max conductor'], save_to_txt=save_to_txt)
