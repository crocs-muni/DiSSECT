from dissect.traits import Trait

TIMEOUT_DURATION = 30


class SmallPrimeOrderTrait(Trait):
    NAME = "small_prime_order"
    DESCRIPTION = (
        "Multiplicative orders of small primes modulo the prime-subgroup order."
    )
    INPUT = {"l": (int, "Small prime")}
    OUTPUT = {
        "order": (int, "Order"),
        "complement_bit_length": (int, "Complement bit length"),
    }
    DEFAULT_PARAMS = {"l": [2, 3, 5, 7, 11, 13]}

    def compute(curve, params):
        """
        Computes the multiplicative order of l (small prime) modulo curve cardinality and bit length of the index of the
        multiplicative subgroup generated by l Returns a dictionary
        """
        from sage.all import Integers, ZZ, euler_phi
        from dissect.utils.utils import timeout

        card = curve.cardinality()
        try:
            assert card.gcd(params["l"]) == 1
            mul_ord = timeout(
                lambda x: x.multiplicative_order(),
                [Integers(card)(params["l"])],
                timeout_duration=TIMEOUT_DURATION,
            )
            euler_phi_card = timeout(
                lambda x: euler_phi(x[0]) * euler_phi(x[1]),
                [(curve.order(), curve.cofactor())],
                timeout_duration=TIMEOUT_DURATION * 0.5,
            )
            complement_bit_length = ZZ(euler_phi_card / mul_ord).nbits()
        except (TypeError, AssertionError):
            mul_ord = None
            complement_bit_length = None
        curve_results = {
            "order": mul_ord,
            "complement_bit_length": complement_bit_length,
        }
        return curve_results


def test_small_prime_order():
    assert True
