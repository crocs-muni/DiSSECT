load("../curve_handler.sage")
load("test_interface.sage")

def embedding_degree_q(q, l):
    '''returns embedding degree with respect to q'''
    return Mod(q,l).multiplicative_order()

def embedding_degree(E, l):
    '''returns relative embedding degree with respect to E'''
    q = (E.base_field()).order()
    return embedding_degree_q(q, l)

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

# Computes the smallest extension which contains a nontrivial l-torsion point
# Returns the degree
def find_least_torsion(E, l):
#    print(r)
    # Trial and error through divisors of l^2-1
    for deg in divisors(l^2-1):
        if ext_card(E, deg) % l == 0:
#             assert deg in [1, (l-1)/2, (l^2-1)/2]
            return deg
    return None

# True if the l-torsion is cyclic and False otherwise (bycyclic)
def is_torsion_cyclic(E, l, deg):
    card = ext_card(E, deg)
    assert card % l^2 == 0
    m = ZZ(card / l)
    EE = extend(E, deg)
    for j in [1..5]:
        P = EE.random_element()
        if not (m*P == EE(0)):
            return True
    return False

# Computes the smallest extension which contains full l-torsion subgroup
# Least is the result of find_least_torsion
# Returns the degree
def find_full_torsion(E, l, least):
    p = E.base_field().order()
    q = p^least
    k = embedding_degree_q(q, l)
    # k satisfies l|a^k-1 where a,1 are eigenvalues of Frobenius of extended E
    if k > 1: #i.e. a!=1
        return k * least
    else: #i.e. a==1, we have two options for the geometric multiplicity
        card = ext_card(E, least)
        if (card % l^2) == 0 and not is_torsion_cyclic(E, l, least): # geom. multiplicity is 2
            return least
        else: # geom. multiplicity is 1
            return l * least 

# Computes k1,k2, k2/k1 where k2(k1) is the smallest extension containing all(some) l-torsion points
# Returns a triple
def find_torsions(E, l):
    least = find_least_torsion(E, l)
    if least == l^2-1:
        full = least
    else:
        full = find_full_torsion(E, l, least)
    return (least, full, ZZ(full/least))

# Computes find_torsions for all l<l_max and returns a dictionary
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
