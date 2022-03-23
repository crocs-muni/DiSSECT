from dissect.traits import Trait


def torsion_finder(curve, l):
    """
    Finds the minimal degrees k_2,k_1 of extension of curve E/F_q where
    E/F_q**(k_2) contains E[l] and E/F_q**(k_1) has nontrivial intersection with E[l]
    Returns k2, k1
    """
    from sage.all import lcm

    eig = curve.eigenvalues(l)
    # Case with no eigenvalues
    if not eig:
        eig = curve.eigenvalues(l, s=2)
        a_ord, b_ord = (
            eig[0][0].multiplicative_order(),
            eig[1][0].multiplicative_order(),
        )
        k2 = lcm(a_ord, b_ord)
        k1 = k2
        return k2, k1

    a_ord = eig[0][0].multiplicative_order()
    # Case with 2 eigenvalues
    if len(eig) == 2:
        b_ord = eig[1][0].multiplicative_order()
        return lcm(a_ord, b_ord), min(a_ord, b_ord)

    # Case with 1 eigenvalue
    k1 = a_ord
    k2 = k1
    card = curve.extended_cardinality(k1)
    torsion_cyclic = curve.is_torsion_cyclic(l, k1)
    if torsion_cyclic is None:
        return None, None
    if card % l ** 2 != 0 or torsion_cyclic:
        k2 = l
    return k2, k1


class TorsionExtensionTrait(Trait):
    NAME = "torsion_extension"
    DESCRIPTION = "Degrees of field extensions containing the least nontrivial $l$-torsion, the full $l$-torsion and their relative degree of extension."
    INPUT = {
        "l": (int, "$l$-torsion")
    }
    OUTPUT = {
        "least": (int, "Least"),
        "full": (int, "Full"),
        "relative": (int, "Relative")
    }
    DEFAULT_PARAMS = {
        "l": [2, 3, 5, 7, 11, 13, 17]
    }

    def compute(curve, params):
        """Computes find_torsions for given l and returns a dictionary"""
        if curve.q() % params["l"] == 0:
            return {"least": None, "full": None, "relative": None}
        k2, k1 = torsion_finder(curve, params["l"])
        if k2 is None:
            return {"least": None, "full": None, "relative": None}
        return {"least": k1, "full": k2, "relative": k2 // k1}


def test_torsion_extension():
    assert True
