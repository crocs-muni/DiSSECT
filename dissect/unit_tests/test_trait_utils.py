import unittest
import dissect.traits.trait_utils as tu
from sage.all import GF, EllipticCurve_from_j, EllipticCurve, ZZ
from dissect.utils.custom_curve import customize_curve

timeout = 0.0001
p, q, r = 101, 103, 107
n = -p * q ** 2 * r ** 3
P, Q = 754137465922759386220603910483, 929875893390950029700007784307
N = P * Q ** 2

F = GF(101)
E = EllipticCurve_from_j(F(1))
Fbin = GF(2 ** 10)
bin_coefs = [1, 1, 0, 0, 1]
binE = EllipticCurve(Fbin, bin_coefs)
deg = 3


class TestTraitUtils(unittest.TestCase):
    def test_ext_card(self):
        self.assertEqual(1073731736, tu.ext_card(customize_curve(binE), deg))
        self.assertEqual(1029924, tu.ext_card(customize_curve(E), deg))

    def test_ext_trace(self):
        self.assertEqual(10089, tu.ext_trace(customize_curve(binE), deg))
        self.assertEqual(378, tu.ext_trace(customize_curve(E), deg))

    def test_ext_disc(self):
        self.assertEqual(-4193179375, tu.ext_disc(customize_curve(binE), deg))
        self.assertEqual(-3978320, tu.ext_disc(customize_curve(E), deg))

    def test_extend(self):
        Ex = tu.extend(customize_curve(binE), deg)
        self.assertEqual(bin_coefs, [ZZ(a) for a in Ex.a_invariants()])
        self.assertEqual(Fbin.order() ** deg, Ex.base_field().order())

        Ex = tu.extend(customize_curve(E), deg)
        self.assertEqual(F.order() ** deg, Ex.base_field().order())
        self.assertEqual(E.change_ring(Ex.base_field()), Ex)

    def test_is_torsion_cyclic(self):
        F = GF(101)
        E = EllipticCurve_from_j(F(10))
        self.assertTrue(tu.is_torsion_cyclic(customize_curve(E), l=5, deg=1))
        E = EllipticCurve_from_j(F(4))
        self.assertTrue(tu.is_torsion_cyclic(customize_curve(E), l=5, deg=1))
        E = EllipticCurve_from_j(F(11))
        self.assertFalse(tu.is_torsion_cyclic(customize_curve(E), l=5, deg=1))

    def test_embedding_degree_q(self):
        self.assertEqual(51, tu.embedding_degree_q(101 ** 2, 103))

    def test_factorization(self):
        self.assertEqual([p, q, q], tu.factorization(p * q ** 2))
        self.assertEqual([p, q, q], tu.factorization(p * q ** 2, use_ecm=False))
        self.assertEqual([p, q, q], tu.factorization(-p * q ** 2))
        self.assertEqual(
            "NO DATA (timed out)",
            tu.factorization(N, timeout_duration=timeout, use_ecm=False),
        )

    def test_squarefree_part(self):
        self.assertEqual(-p * r, tu.squarefree_part(n))
        self.assertEqual(-p * r, tu.squarefree_part(n, use_ecm=False))
        self.assertEqual(
            "NO DATA (timed out)",
            tu.squarefree_part(N, timeout_duration=timeout, use_ecm=False),
        )

    def test_squarefree_and_factorization(self):
        self.assertEqual(
            (-p * r, [p, q, q, r, r, r]), tu.squarefree_and_factorization(n)
        )
        self.assertEqual(
            (-p * r, [p, q, q, r, r, r]),
            tu.squarefree_and_factorization(n, use_ecm=False),
        )
        self.assertEqual(
            "NO DATA (timed out)",
            tu.squarefree_and_factorization(N, timeout_duration=timeout, use_ecm=False),
        )

    def test_square_part(self):
        self.assertEqual((q * r) ** 2, tu.square_part(n))
        self.assertEqual((q * r) ** 2, tu.square_part(n, use_ecm=False))
        self.assertEqual(
            "NO DATA (timed out)",
            tu.square_part(N, timeout_duration=timeout, use_ecm=False),
        )

    def test_square_part_square_root(self):
        self.assertEqual((q * r), tu.square_part_square_root(n))
        self.assertEqual((q * r), tu.square_part_square_root(n, use_ecm=False))
        self.assertEqual(
            "NO DATA (timed out)",
            tu.square_part_square_root(N, timeout_duration=timeout, use_ecm=False),
        )


if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
