import unittest
from dissect.utils.utils import Factorization

timeout = 0.0001
p, q, r = 101, 103, 107
n = -p * q ** 2 * r ** 3
P, Q = 754137465922759386220603910483, 929875893390950029700007784307
N = P * Q ** 2


class TestTraitUtils(unittest.TestCase):

    def test_factorization(self):
        x = p * q ** 2
        self.assertEqual([p, q, q], Factorization(x).factorization())
        self.assertEqual([p, q, q], Factorization(x, use_ecm=False).factorization())
        self.assertEqual([p, q, q], Factorization(-x).factorization())
        self.assertEqual("NO DATA (timed out)",
                         Factorization(N, timeout_duration=timeout, use_ecm=False).factorization())

    def test_squarefree_part(self):
        self.assertEqual(-p * r, Factorization(n).squarefree())
        self.assertEqual(-p * r, Factorization(n, use_ecm=False).squarefree())
        self.assertEqual("NO DATA (timed out)",
                         Factorization(N, timeout_duration=timeout, use_ecm=False).factorization())

    def test_square_part(self):
        self.assertEqual((q * r) ** 2, Factorization(n).square())
        self.assertEqual((q * r) ** 2, Factorization(n,use_ecm=False).square())
        self.assertEqual("NO DATA (timed out)",Factorization(N, timeout_duration=timeout, use_ecm=False).square())

    def test_square_part_square_root(self):
        self.assertEqual((q * r), Factorization(n).square_root())
        self.assertEqual((q * r), Factorization(n,use_ecm=False).square_root())
        self.assertEqual("NO DATA (timed out)",Factorization(N, timeout_duration=timeout, use_ecm=False).square_root())

    def test_addition(self):
        u,v = 11,13
        s = Factorization(p*q)+Factorization(u*v*v)
        self.assertEqual(s.factorization(),[u,v,v,p,q])
        s = Factorization(n)+Factorization(p)
        self.assertEqual(s.factorization(),[p,p,q,q,r,r,r])
        s = Factorization(N, timeout_duration=timeout, use_ecm=False)+Factorization(p*q)
        self.assertTrue(s.timeout())

if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
