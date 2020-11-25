from sage.all import PolynomialRing, ZZ, GF, EllipticCurve,log

from curve_analyzer.tests.test_interface import pretty_print_results, compute_results


def ext_card(E, order, deg):
    '''returns curve cardinality over deg-th relative extension'''
    card_low = order
    q = (E.base_field()).order()
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


def is_torsion_cyclic(E, q,order, l, deg,field):
    card = ext_card(E, order, deg)
    assert card % l ** 2 == 0
    m = ZZ(card / l)
    EE = extend(E,q,deg,field)
    for j in range(1, 6):
        P = EE.random_element()
        if not (m * P == EE(0)):
            return True
    return False


# Computes the eigenvalues of Frobenius endomorphism in F_l, or in F_l if s=2
def eigenvalues(curve, l, s=1):
    x = PolynomialRing(GF(l ** s), 'x').gen()
    q = curve.q
    t = curve.trace
    f = x ** 2 - t * x + q
    return f.roots()


# Finds the minimal degrees i_2,i_1 of extension of curve E/F_q where
# E/F_q**(i_2) - all l+1 isogenies are rational, E/F_q**(i_1) - at least 1 isogeny is rational
# Returns i2, i1
def i_finder(curve, l):
    eig = eigenvalues(curve, l)
    # Case with no eigenvalues
    if not eig:
        eig = eigenvalues(curve, l, s=2)
        a, b = eig[0][0], eig[1][0]
        i2 = (a * b ** (-1)).multiplicative_order()
        i1 = i2
        return i2, i1

    a = eig[0][0]
    # Case with 2 eigenvalues
    if len(eig) == 2:
        b = eig[1][0]
        i1 = 1
        i2 = (a * b ** (-1)).multiplicative_order()
        return i2, i1
    # Case with 1 eigenvalue
    i1 = 1
    i2 = 1
    deg = a.multiplicative_order()
    E = curve.EC
    card = ext_card(E, curve.order*curve.cofactor, deg)
    if card % l ** 2 != 0 or is_torsion_cyclic(E,curve.q, curve.order*curve.cofactor, l, deg,curve.field):
        i2 *= l
    return i2, i1


# Computes i2,i1 (see i_finder) for all primes l<l_max
# Returns a dictionary (keys: 'least' (i1), 'full' (i2), 'relative' (i2/i1))
def a24_curve_function(curve, l):
    curve_results = {}
    try:
        i2, i1 = i_finder(curve, l)
        least, full, relative = i1, i2, i2 // i1
    except (ArithmeticError, TypeError, ValueError) as e:
        least, full, relative = None, None, None

    curve_results['least'] = least
    curve_results['full'] = full
    curve_results['relative'] = relative
    return curve_results


def compute_a24_results(curve_list, desc='', verbose = False):
    compute_results(curve_list, 'a24', a24_curve_function, desc=desc, verbose=verbose)


def get_a24_captions(results):
    captions = ['least', 'full', 'relative']
    return captions


def select_a24_results(curve_results):
    keys = ['least', 'full', 'relative']
    selected_results = []
    for key in keys:
        selected_key = []
        for x in curve_results:
            selected_key.append(x[key])
        selected_results.append(selected_key)
    return selected_results


def pretty_print_a24_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a24', get_a24_captions, select_a24_results, save_to_txt=save_to_txt)
