from typing import List
from sage.all import factor
from dissect.utils.utils import timeout
from dissect.utils.custom_curve import CustomCurve
from dissect.traits import Trait

TIMEOUT_DURATION = 30

class A22(Trait):
    NAME = "a22"
    DESCRIPTION = "Factorizations of small division polynomials."
    INPUT = {
        "l": (int, "Prime")
    }
    OUTPUT = {
        "factorization": (List[List[int]], "Factorization of $l$-th division polynomial"),
        "len": (int, "Length")
    }
    DEFAULT_PARAMS = {
        "l": [2, 3, 5]
    }

    def compute(curve: CustomCurve, params):
        """
        Computation factorization of l-th division polynomial
        More precisely, computes a list of tuple [a,b]
        where b is the number of irreducible polynomials of degree a in the factorization (with multiplicity)
        """
        factors = timeout(factor, [curve.ec().division_polynomial(params["l"])], timeout_duration=TIMEOUT_DURATION)
        if isinstance(factors, str):
            return {"factorization":None, "len": None}
        fact = map(lambda x: (x[0].degree(), x[1]), factors)
        result = {}
        for deg, ex in fact:
            if deg not in result:
                result[deg] = 0
            result[deg] += ex
        # Converts tuples to lists for json
        result = [list(i) for i in result.items()]
        return {"factorization": result, "len": len(result)}
