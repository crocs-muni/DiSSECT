from sage.all import ZZ, PolynomialRing, GF, Integers,log, EllipticCurve

from curve_analyzer.tests.test_interface import pretty_print_results, compute_results


def embedding_degree_q(q, l):
    '''returns embedding degree with respect to q'''
    return (Integers(l)(q)).multiplicative_order()


def ext_card(E, q, card_low, deg):
    '''returns curve cardinality over deg-th relative extension'''
    tr = q + 1 - card_low
    s_old, s_new = 2, tr
    for i in range(2, deg + 1):
        s_old, s_new = s_new, tr * s_new - q * s_old
    card_high = q ** deg + 1 - s_new
    return card_high

def stupid_coerce_K_to_L(element,K,L):
    name_K = str(K.gen())
    name_L = str(L.gen())
    return L(str(element).replace(name_K,name_L))

def extend(E, q, deg,field):
    '''returns curve over deg-th relative extension; does not seem to work for binary curves'''
    if q%2!=0:
        R = field['x']
        pol = R.irreducible_element(deg)
        Fext = GF(q ** deg, name='z', modulus=pol)
        return E.base_extend(Fext)
    K = field
    charac = K.characteristic()
    R = GF(charac)['x']
    ext_deg = q ** deg
    pol = R.irreducible_element(deg*(log(q, charac)))
    Kext = GF(ext_deg, name='ex', modulus=pol)
    gKext = Kext.gen()

    h = gKext ** ((ext_deg - 1) // (q - 1))
    assert charac ** (h.minpoly().degree()) == q
    H = GF(q, name='h', modulus=h.minpoly())
    inclusion = H.hom([h])

    new_coefficients = [inclusion(stupid_coerce_K_to_L(a, K, H)) for a in E.a_invariants()]
    EE = EllipticCurve(Kext, new_coefficients)
    return EE


# Computes the smallest extension which contains a nontrivial l-torsion point
# Returns the degree
def find_least_torsion(E, q, order, l):
    x = PolynomialRing(GF(l ** 2), 'x').gen()
    t = q + 1 - order

    f = x ** 2 - t * x + q

    roots = [r[0] for r in f.roots() for _ in range(r[1])]

    return min(roots[0].multiplicative_order(), roots[1].multiplicative_order())


# True if the l-torsion is cyclic and False otherwise (bycyclic)
def is_torsion_cyclic(E, q, order, l, deg,field):
    card = ext_card(E, q, order, deg)
    m = ZZ(card / l)
    EE = extend(E, q, deg,field)
    for j in range(1, 6):
        P = EE.random_element()
        if not (m * P == EE(0)):
            return True
    return False


# Computes the smallest extension which contains full l-torsion subgroup
# Least is the result of find_least_torsion
# Returns the degree
def find_full_torsion(E, q, order, l, least,field):
    q_least = q ** least
    k = embedding_degree_q(q_least, l)
    # k satisfies l|a^k-1 where a,1 are eigenvalues of Frobenius of extended E
    if k > 1:  # i.e. a!=1
        return k * least
    else:  # i.e. a==1, we have two options for the geometric multiplicity
        card = ext_card(E, q, order, least)
        if (card % l ** 2) == 0 and not is_torsion_cyclic(E, q, order, l, least,field):  # geom. multiplicity is 2
            return least
        else:  # geom. multiplicity is 1
            return l * least

        # Computes k1,k2, k2/k1 where k2(k1) is the smallest extension containing all(some) l-torsion points


# Returns a triple
def find_torsions(E, q, order, l, field):
    least = find_least_torsion(E, q, order, l)
    if least == l ** 2 - 1:
        full = least

    else:
        full = find_full_torsion(E, q, order, l, least, field)

    return least, full, ZZ(full / least)


# Computes find_torsions for given l and returns a dictionary
def a05_curve_function(curve, l):
    E = curve.EC
    q = curve.q
    order = curve.order * curve.cofactor
    curve_results = {}

    try:
        least, full, relative = find_torsions(E, q, order, l,curve.field )

    except (ArithmeticError, TypeError, ValueError) as e:
        least, full, relative = None, None, None

    curve_results['least'] = least
    curve_results['full'] = full
    curve_results['relative'] = relative

    return curve_results


def compute_a05_results(curve_list, desc=''):
    compute_results(curve_list, 'a05', a05_curve_function, desc=desc)


def get_a05_captions(results):
    captions = ['least', 'full', 'relative']
    return captions


def select_a05_results(curve_results):
    keys = ['least', 'full', 'relative']
    selected_results = []
    for key in keys:
        selected_key = []
        for x in curve_results:
            selected_key.append(x[key])
        selected_results.append(selected_key)
    return selected_results


def pretty_print_a05_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a05', get_a05_captions, select_a05_results, save_to_txt=save_to_txt)
