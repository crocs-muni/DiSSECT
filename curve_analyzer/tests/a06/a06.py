from sage.all import kronecker
from curve_analyzer.tests.test_interface import pretty_print_results, compute_results

def ext_card(E, q, card_low, deg):
    '''returns curve cardinality over deg-th relative extension'''
    tr = q + 1 - card_low
    s_old, s_new = 2, tr
    for i in range(2, deg + 1):
        s_old, s_new = s_new, tr * s_new - q * s_old
    card_high = q ** deg + 1 - s_new
    return card_high

def ext_cm_disc(E, q, card_low, deg):
    '''returns the CM discriminant (up to a square) over deg-th relative extension'''
    card_high = ext_card(E, q, card_low, deg)
    ext_tr = q ** deg + 1 - card_high
    return ext_tr ** 2 - 4 * q ** deg

def a06_curve_function(curve, l, deg):
    '''returns the Kronecker symbol of the CM discriminant over the deg-th relative extension with respect to l'''
    E = curve.EC
    q = curve.q
    curve_results = {}
    order = curve.order * curve.cofactor
    cm_disc = ext_cm_disc(E, q, order, deg)
    while cm_disc % l**2 == 0:
        cm_disc = cm_disc / l**2

    if l == 2 and cm_disc % 4 != 1:
        curve_results["kronecker"] = 0
    else:
        curve_results["kronecker"] = kronecker(cm_disc, l)
    return curve_results

def compute_a06_results(curve_list, desc=''):
    compute_results(curve_list, 'a06', a06_curve_function, desc=desc)

def get_a06_captions(results):
    # TO DO
    pass

def select_a06_results(curve_results):
    # TO DO
    pass

def pretty_print_a06_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a06', get_a06_captions, select_a06_results, save_to_txt=save_to_txt)
