load("../curve_handler.sage")
load("test_interface.sage")

def a6_curve_function(curve):
    E = curve.EC
    t = curve.trace
    q = curve.q
    curve_results = {'cm_disc': {}, 'factorization': {}}
    d = t^2 - 4 * q
    curve_results['cm_disc'] = d
    curve_results['factorization'] = list(factor(d))
    curve_results['max_conductor'] = ZZ(sqrt(d/d.squarefree_part()))
    return curve_results

def compute_a6_results(order_bound = 256, overwrite = False):
    parameters = {}
    compute_results('a6', a6_curve_function, parameters, order_bound, overwrite)

def pretty_print_a6_results(save_to_txt = True):
    pretty_print_results('a6', [['factorization'], ['max_conductor']], ['CM disc factorization', 'max conductor'], save_to_txt = save_to_txt)


p = c.EC.base_field().order()
n = 1
print(n*p.nbits())
F = GF(p^n)
E = c.EC.change_ring(F)
print(E.order())
c.cofactor