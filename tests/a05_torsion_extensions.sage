load("../curve_handler.sage")
load("test_interface.sage")

def embedding_degree_q(q, r):
    '''returns embedding degree with respect to q'''
    return Mod(q,r).multiplicative_order()

def embedding_degree(E, r):
    '''returns relative embedding degree with respect to E'''
    q = (E.base_field()).order()
    return embedding_degree_q(q, r)

def ext_card(E, deg):
    '''returns curve cardinality over deg-th relative extension'''
    card_low = E.cardinality()
    q = (E.base_field()).order()
    tr = q + 1 - card_low
    s_old, s_new = 2, tr
    for i in [2..deg]:
        s_old, s_new = s_new, tr * s_new - q * s_old
    card_high = q^deg + 1 - s_new
    return card_high

def extend(E, deg):
    '''returns curve over deg-th relative extension; does not seem to work for binary curves'''
    q = E.base_field().order()
    R.<x> = E.base_field()[]
    pol = R.irreducible_element(deg)
    Fext = GF(q^deg, name = 'z', modulus = pol)
    EE = E.base_extend(Fext)
    return EE

def find_least_torsion(E, r):
    print(r)
    for deg in divisors(r^2-1):
        if ext_card(E, deg) % r == 0:
#             assert deg in [1, (r-1)/2, (r^2-1)/2]
            return deg
    return None

def is_torsion_cyclic(E, r, deg):
    card = ext_card(E, deg)
    assert card % r^2 == 0
    m = ZZ(card / r)
    EE = extend(E, deg)
    for j in [1..5]:
        P = EE.random_element()
        if not (m*P == EE(0)):
            return True
    return False

def find_full_torsion(E, r, least):
    p = E.base_field().order()
    q = p^least
    k = embedding_degree_q(q, r)
    if k > 1:
        return k * least
    else:
        card = ext_card(E, least)
        if (card % r^2) == 0 and not is_torsion_cyclic(E, r, least):
            return least
        else:
            return r * least

def find_torsions(E, r):
    least = find_least_torsion(E, r)
    if least == r^2-1:
        full = least
    else:
        full = find_full_torsion(E, r, least)
    return (least, full, ZZ(full/least))

def a5_curve_function(curve, l_max):
    E = curve.EC
    curve_results = {'least': [], 'full': [], 'relative': []}

    for l in prime_range(l_max):
        try:
            least, full, relative = find_torsions(E, l)
        except (ArithmeticError, TypeError, ValueError) as e:
            least, full, relative = None, None, None
        
        curve_results['least'].append(least)
        curve_results['full'].append(full)
        curve_results['relative'].append(relative)
    return curve_results

def compute_a5_results(l_max = 20, order_bound = 256, overwrite = False, curve_list = curves):
    parameters = {'l_max': l_max}
    compute_results('a5', a5_curve_function, parameters, order_bound, overwrite, curve_list = curve_list)

def pretty_print_a5_results(save_to_txt = True):
    pretty_print_results('a5', [['least'], ['full'], ['relative']], ['least torsion', 'full torsion', 'relative ratio'], save_to_txt = save_to_txt, res_sort_key = lambda x: 1)