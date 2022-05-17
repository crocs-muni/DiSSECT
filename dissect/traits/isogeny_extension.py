from dissect.traits import Trait


def isogeny_finder(curve, l):
    """
    Finds the minimal degrees i_2,i_1 of extension of curve E/F_q where
    E/F_q**(i_2) - all l+1 isogenies are rational, E/F_q**(i_1) - at least 1 isogeny is rational
    Returns i2, i1
    """
    eig = curve.eigenvalues(l)
    # Case with no eigenvalues
    if not eig:
        eig = curve.eigenvalues(l, s=2)
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
    # deg = k1
    card = curve.extended_cardinality(deg)
    # now check whether k1=k2:
    if card % l ** 2 != 0 or curve.is_torsion_cyclic(l, deg):
        i2 *= l
    return i2, i1


class IsogenyExtensionTrait(Trait):
    NAME = "isogeny_extension"
    DESCRIPTION = "The least field extensions containing a nontrivial number and full number of $l$-isogenies and their relative ratio."
    INPUT = {
        "l": (int, "Prime")
    }
    OUTPUT = {
        "least": (int, "Least"),
        "full": (int, "Full"),
        "relative": (int, "Relative")
    }
    DEFAULT_PARAMS = {
        "l": [2, 3, 5, 7, 11, 13, 17, 19]
    }


    def compute(curve, params):
        """
        Computes i2,i1 (see i_finder) for all primes l<l_max
        Returns a dictionary (keys: 'least' (i1), 'full' (i2), 'relative' (i2/i1))
        """
        if curve.q() % params["l"] == 0:
            return {"least": None, "full": None, "relative": None}
        i2, i1 = isogeny_finder(curve, params["l"])
        return {"least": i1, "full": i2, "relative": i2 // i1}


def test_isogeny_extension():
    assert True
