from sage.all import euler_phi, ZZ

from dissect.utils.custom_curve import CustomCurve
from dissect.traits import Trait


class A07(Trait):
    NAME = "a07"
    DESCRIPTION = "The complement of the embedding degree, i.e. $(n-1)/e$ where $n$ is the prime-subgroup order and $e$ is the embedding degree."
    INPUT = {}
    OUTPUT = {
        "embedding_degree_complement": (int, "Embedding degree complement"),
        "complement_bit_length": (int, "Complement bit length")
    }
    DEFAULT_PARAMS = {}

    def compute(curve: CustomCurve, params):
        """Computes the embedding degree (with respect to the generator order) and its complement"""
        q = curve.q()
        if q.nbits() > 300:
            return {"embedding_degree_complement":None,"complement_bit_length":None}
        l = curve.order()
        embedding_degree = curve.embedding_degree()
        embedding_degree_complement = ZZ(euler_phi(l) / embedding_degree)
        complement_bit_length = embedding_degree_complement.nbits()
        curve_results = {
            "embedding_degree_complement": embedding_degree_complement,
            "complement_bit_length": complement_bit_length,
        }
        return curve_results
