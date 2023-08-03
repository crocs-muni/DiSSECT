from typing import List
from dissect.traits import Trait

TRAIT_TIMEOUT = 20


class TraceFactorizationTrait(Trait):
    NAME = "trace_factorization"
    DESCRIPTION = "Factorization of trace in field extensions."
    INPUT = {"deg": (int, "Integer")}
    OUTPUT = {
        "trace": (int, "Trace"),
        "trace_factorization": (List[int], "Factorization of trace"),
        "number_of_factors": (int, "Number of factors"),
    }
    DEFAULT_PARAMS = {"deg": [1, 2]}

    def compute(self, curve, params):
        """Computation of the trace in an extension together with its factorization"""
        from dissect.utils.utils import Factorization

        trace = curve.extended_trace(params["deg"])
        f = Factorization(trace, timeout_duration=TRAIT_TIMEOUT)
        num_of_factors = (
            f.timeout_message() if f.timeout() else len(list(set(f.factorization())))
        )
        curve_results = {
            "trace": curve.trace(),
            "trace_factorization": f.factorization(),
            "number_of_factors": num_of_factors,
        }
        return curve_results


def test_trace_factorization():
    assert True
