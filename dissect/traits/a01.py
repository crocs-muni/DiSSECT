from dissect.traits import Trait

# global time for one group computation
TIME = 150

def smith_normal_form(ext_ec):
    """Compute the smith normal form, (n1, n2) where n1 divides n2."""
    from sage.all import gcd, lcm

    gens = ext_ec.abelian_group().gens()
    if len(gens) == 1:
        return 1, gens[0].order()
    ord1, ord2 = gens[0].order(), gens[1].order()
    return gcd(ord1, ord2), lcm(ord1, ord2)


class A01(Trait):
    NAME = "a01"
    DESCRIPTION = "The Smith normal form of the group in an extension field, i.e. $(n_1,n_2)$ where $n_1$ divides $n_2$."
    MOTIVATION = "The group structure is not an isogeny invariant."
    INPUT = {
        "r": (int, "Integer $r$"),
    }
    OUTPUT = {
        "ord1": (int, "Order 1"),
        "ord2": (int, "Order 2"),
    }
    DEFAULT_PARAMS = {
        "deg": [1, 2]
    }

    def compute(self, curve, params):
        """Computes the orders of the two generators of the curve over the deg-th relative extension."""
        from dissect.utils.utils import timeout

        curve_results = {}
        ext_ec = curve.extended_ec(params["deg"])
        result = timeout(smith_normal_form, [ext_ec], timeout_duration=TIME)
        if isinstance(result, str):
            result = result, result
        curve_results["ord1"], curve_results["ord2"] = result
        return curve_results


def test_a01():
    assert True
