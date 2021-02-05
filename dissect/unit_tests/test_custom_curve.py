import unittest

from sage.all import GF

from dissect.utils.custom_curve import twisted_edwards_to_short_weierstrass, twisted_edwards_to_montgomery, \
    CustomCurve

# Test vectors: https://tools.ietf.org/id/draft-struik-lwip-curve-representations-00.html#rfc.appendix.C.3

p = 2 ** 255 - 19
F = GF(p)
a = -1
d = F(-121665) / (121666)
x = 15112221349535400772501151409588531511454012693041857206046113283949847762202
y = F(4) / (5)

Wei25519 = {'a': 19298681539552699237261830834781317975544997444273427339909597334573241639236,
            'b': 55751746669818908907645289078257140818241103727901012315294400837956729358436,
            'x': 19298681539552699237261830834781317975544997444273427339909597334652188435546,
            'y': 14781619447589544791020593568409986887264606134616475288964881837755586237401}

Mon25519 = {'A': 486662,
            'B': 1,
            'u': 9,
            'v': 14781619447589544791020593568409986887264606134616475288964881837755586237401
            }
B1 = CustomCurve(
    {
        "name": "sect163k1",
        "category": "secg",
        "desc": "",
        "oid": "1.3.132.0.1",
        "field": {
            "type": "Binary",
            "poly": [
                {
                    "power": 163,
                    "coeff": "0x01"
                },
                {
                    "power": 7,
                    "coeff": "0x01"
                },
                {
                    "power": 6,
                    "coeff": "0x01"
                },
                {
                    "power": 3,
                    "coeff": "0x01"
                },
                {
                    "power": 0,
                    "coeff": "0x01"
                }
            ],
            "bits": 163,
            "degree": 163
        },
        "form": "Weierstrass",
        "params": {
            "a": {"raw": "0x000000000000000000000000000000000000000001"},
            "b": {"raw": "0x000000000000000000000000000000000000000001"}
        },
        "generator": {
            "x": {"raw": "0x02fe13c0537bbc11acaa07d793de4e6d5e5c94eee8"},
            "y": {"raw": "0x0289070fb05d38ff58321f2e800536d538ccdaa3d9"}
        },
        "order": "0x04000000000000000000020108a2e0cc0d99f8a5ef",
        "cofactor": "0x2",
        "aliases": [
            "nist/K-163"
        ],
        "characteristics": {
            "discriminant": "1",
            "j_invariant": "1",
            "trace_of_frobenius": "-4845466632539410776804317",
            "anomalous": False,
            "supersingular": False,
            "cm_disc": "46768052394588893382517919492387689168400618179549",
            "conductor": "1"
        }
    })

B1_results = {"cofactor": 2, "a": 1, "b": 1, "order": 0x04000000000000000000020108A2E0CC0D99F8A5EF,
              "gen_x": 0x02fe13c0537bbc11acaa07d793de4e6d5e5c94eee8,
              "gen_y": 0x0289070fb05d38ff58321f2e800536d538ccdaa3d9}


class TestCustomCurve(unittest.TestCase):

    def test_Ed_to_Wei(self):
        result = twisted_edwards_to_short_weierstrass(F, a, d, x, y)
        self.assertEqual(result[0], Wei25519['a'],
                         "Should be " + str(Wei25519['a']))
        self.assertEqual(result[1], Wei25519['b'],
                         "Should be " + str(Wei25519['b']))
        self.assertEqual(result[2], Wei25519['x'],
                         "Should be " + str(Wei25519['x']))
        self.assertEqual(result[3], Wei25519['y'],
                         "Should be " + str(Wei25519['y']))

    def test_Ed_to_Mon(self):
        result = twisted_edwards_to_montgomery(F, a, d, x, y)
        self.assertEqual(result[0], Mon25519['A'],
                         "Should be " + str(Mon25519['A']))
        self.assertEqual(result[1], Mon25519['B'],
                         "Should be " + str(Mon25519['B']))
        self.assertEqual(result[2], Mon25519['u'],
                         "Should be " + str(Mon25519['u']))
        self.assertEqual(result[3], Mon25519['v'],
                         "Should be " + str(Mon25519['v']))

    def test_B1_constructor(self):
        self.assertEqual(B1.cofactor, B1_results["cofactor"], "Should be " + str(B1_results["cofactor"]))
        self.assertEqual(B1.EC.a2(), B1_results["a"], "Should be " + str(B1_results["a"]))
        self.assertEqual(B1.EC.a6(), B1_results["b"], "Should be " + str(B1_results["b"]))
        self.assertEqual(B1.order, B1_results["order"], "Should be " + str(B1_results["order"]))
        self.assertEqual(B1.x, B1_results["gen_x"], "Should be " + str(B1_results["gen_x"]))
        self.assertEqual(B1.y, B1_results["gen_y"], "Should be " + str(B1_results["gen_y"]))


if __name__ == '__main__':
    unittest.main()
    print("Everything passed")
