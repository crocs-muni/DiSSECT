load("../curve_handler.sage")
load("test_interface.sage")

def a2_curve_function(curve):
    E = curve.EC
    t = curve.trace
    q = curve.q
    curve_results = {'cm_disc': {}, 'factorization': {}}
    d = t^2 - 4 * q
    curve_results['cm_disc'] = d
    curve_results['factorization'] = list(factor(d))
    curve_results['max_conductor'] = ZZ(sqrt(d/d.squarefree_part()))
    return curve_results

def compute_a2_results(order_bound = 256, overwrite = False):
    parameters = {}
    compute_results('a2', a2_curve_function, parameters, order_bound, overwrite)

def pretty_print_a2_results(save_to_txt = True):
    pretty_print_results('a2', [['factorization'], ['max_conductor']], ['CM disc factorization', 'max conductor'], save_to_txt = save_to_txt)