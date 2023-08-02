from dissect.traits import Trait


class EmbeddingTrait(Trait):
    NAME = "embedding"
    DESCRIPTION = "The complement of the embedding degree, i.e. $(n-1)/e$ where $n$ is the prime-subgroup order and $e$ is the embedding degree."
    INPUT = {}
    OUTPUT = {
        "embedding_degree_complement": (int, "Embedding degree complement"),
        "complement_bit_length": (int, "Complement bit length"),
    }
    DEFAULT_PARAMS = {}

    def compute(curve, params):
        """Computes the embedding degree (with respect to the generator order) and its complement"""
        from sage.all import euler_phi, ZZ

        q = curve.q()
        if q.nbits() > 300:
            return {"embedding_degree_complement": None, "complement_bit_length": None}
        l = curve.order()
        embedding_degree = curve.embedding_degree()
        embedding_degree_complement = ZZ(euler_phi(l) / embedding_degree)
        complement_bit_length = embedding_degree_complement.nbits()
        curve_results = {
            "embedding_degree_complement": embedding_degree_complement,
            "complement_bit_length": complement_bit_length,
        }
        return curve_results


def test_embedding():
    assert True
