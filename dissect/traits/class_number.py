from dissect.traits import Trait


class ClassNumberTrait(Trait):
    NAME = "class_number"
    DESCRIPTION = "Upper and lower bound for the class number of the CM-field."
    INPUT = {}
    OUTPUT = {"upper": (int, "Upper"), "lower": (int, "Lower")}
    DEFAULT_PARAMS = {}

    def compute(self, curve, params):
        """
        Computes the lower and upper bound of class number of the maximal order of the endomorphism algebra

        Upper bound:
        Inequality class number<= sqrt(d)*log(d)*constant (see below)
        #https://en.wikipedia.org/wiki/Class_number_formula#Dirichlet_class_number_formula
        #https://math.stackexchange.com/questions/1887252/class-number-upper-bound-for-imaginary-quadratic-fields

        Lower bound:
        https://mathworld.wolfram.com/ClassNumber.html
        """
        from sage.all import ceil, log, sqrt, pi, floor, ln, gcd

        cm_disc = curve.cm_discriminant()
        frob_disc_factor = curve.frobenius_disc_factorization()
        if frob_disc_factor.timeout():
            return {
                "upper": frob_disc_factor.timeout_message(),
                "lower": frob_disc_factor.timeout_message(),
            }
        fact_d = [
            f for f, e in frob_disc_factor.factorization(unpack=False) if e % 2 == 1
        ]
        if cm_disc % 4 == 0:
            fact_d.append(2)

        w = {4: 4, 3: 6}.get(-cm_disc, 2)
        upper_bound = ceil(log(-cm_disc) * sqrt(-cm_disc) * w / (2 * pi))

        fact_d = sorted(fact_d)[:-1]
        lower_bound = 1
        for f in fact_d:
            lower_bound *= (1 - floor(2 * sqrt(f)) / (f + 1)) * ln(-cm_disc)
        if gcd(cm_disc, 5077) == 1:
            lower_bound *= 1 / 55
        else:
            lower_bound *= 1 / 7000
        lower_bound = floor(lower_bound)
        curve_results = {"upper": upper_bound, "lower": lower_bound}
        return curve_results


def test_class_number():
    assert True
