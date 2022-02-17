from dissect.utils.utils import Factorization
from dissect.utils.custom_curve import CustomCurve
from dissect.traits import Trait

TRAIT_TIMEOUT = 20


class A25(Trait):
    NAME = "a25"
    DESCRIPTION = "The least field extensions containing a nontrivial number and full number of $l$-isogenies and their relative ratio.",
    INPUT = {
        "l": (int, "Prime")
    }
    OUTPUT = {
        "least": (int, "Least"),
        "full": (int, "Full"),
        "relative": (int, "Relative")
    }
    DEFAULT_PARAMS = {
        "l": [1, 2]
    }


    def compute(curve: CustomCurve, params):
        """Computation of the trace in an extension together with its factorization"""
        trace = curve.extended_trace(params["deg"])
        f = Factorization(trace, timeout_duration=TRAIT_TIMEOUT)
        num_of_factors = f.timeout_message() if f.timeout() else len(list(set(f.factorization())))
        curve_results = {
            "trace": curve.trace(),
            "trace_factorization": f.factorization(),
            "number_of_factors": num_of_factors,
        }
        return curve_results
