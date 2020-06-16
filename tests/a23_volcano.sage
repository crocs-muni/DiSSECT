load("../curve_handler.sage")
load("test_interface.sage")

# Computes the depth of volcano and the degree of the crater subgraph containing E
# Returns a dictionary (keys: 'crater_degree', 'depth')
def a23_curve_function(curve,l):
    E = curve.EC
    t = curve.trace
    q = curve.q
    curve_results = {}
    D = t**2 - 4 * q
    d = D.squarefree_part()
    d = 4*d if d%4!=1 else d
    curve_results['crater_degree'] = kronecker(d,l)+1
    curve_results['depth'] = ZZ.valuation(l)(ZZ(sqrt(D//d)))
    return curve_results

def compute_a23_results(order_bound = 256, overwrite = False, curve_list = curves):
    parameters = {}
    compute_results('a23', a23_curve_function, parameters, order_bound, overwrite, curve_list = curve_list)

def pretty_print_a23_results(save_to_txt = True):
    pretty_print_results('a23', [['crater_degree'], ['depth']], ['crater_degree', 'depth'], save_to_txt = save_to_txt)
