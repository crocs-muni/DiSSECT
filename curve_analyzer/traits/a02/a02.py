from sage.all import ZZ, sqrt, factor, squarefree_part

from curve_analyzer.traits.trait_interface import pretty_print_results, compute_results, timeout

# global time for one factorization
TIME = 10


def ext_trace(q, t, deg):
    a = 2
    b = t
    for _ in range(deg - 1):
        tmp = b
        b = t * b - q * a
        a = tmp
    return b


def a02_curve_function(curve, deg):
    '''
    Computation of d_K (cm_disc), v (max_conductor) and factorization of D where D=t^2-4q = v^2*d_K
    Returns a dictionary (keys: 'cm_disc', 'factorization', 'max_conductor')
    '''
    t = curve.trace
    q = curve.q
    curve_results = {}
    t = ext_trace(q, t, deg)
    q = q ** deg
    D = t ** 2 - 4 * q
    d = squarefree_part(D)
    disc = d
    if d % 4 != 1:
        disc *= 4
    curve_results['cm_disc'] = disc
    t = TIME
    factorization = timeout(factor, [D], timeout_duration=t)
    if factorization == 'NO DATA (timed out)':
        curve_results['factorization'] = []
    else:
        tuples_to_lists = [list(i) for i in list(factorization)]
        curve_results['factorization'] = tuples_to_lists
    curve_results['max_conductor'] = ZZ(sqrt(D / disc))
    return curve_results


def compute_a02_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a02', a02_curve_function, desc=desc, verbose=verbose)


def get_a02_captions(results):
    return ['max_conductor', 'factorization', 'cm_disc']


def select_a02_results(curve_results):
    keys = ['max_conductor', 'factorization', 'cm_disc']
    selected_results = []
    for key in keys:
        for x in curve_results:
            selected_results.append(x[key])
    return selected_results


def pretty_print_a02_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a02', get_a02_captions, select_a02_results, save_to_txt=save_to_txt)
