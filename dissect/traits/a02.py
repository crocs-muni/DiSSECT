from typing import List
from dissect.traits import Trait

class A02(Trait):
    NAME = "a02"
    DESCRIPTION = "Factorization of the discriminant of the Frobenius polynomial, i.e. factorization of  $t^2-4p=v^2d_K$, where $t$ is the trace of Frobenius, $v$ is the maximal conductor and $d_K$ is the CM discriminant."
    MOTIVATION = "A large conductor has interesting implications."
    INPUT = {}
    OUTPUT = {
        "cm_disc": (int, "CM discriminant"),
        "factorization": (List[int], "Factorization of $D = t^2-4p$"),
        "max_conductor": (int, "Maximal conductor $v$")
    }
    DEFAULT_PARAMS = {}

    def compute(curve):
        """
        Computation of d_K (cm_disc), v (max_conductor) and factorization of D where D=t^2-4q = v^2*d_K
        Returns a dictionary (keys: 'cm_disc', 'factorization', 'max_conductor')
        """
        curve_result = {"cm_disc": None, "factorization": None, "max_conductor": None}
        frob_disc_factor = curve.frobenius_disc_factorization()
        if frob_disc_factor.timeout():
            return curve_result
        return {"cm_disc": curve.cm_discriminant(), "factorization": frob_disc_factor.factorization(unpack=True),
                "max_conductor": frob_disc_factor.cm_conductor()}


def test_a02():
    assert True
