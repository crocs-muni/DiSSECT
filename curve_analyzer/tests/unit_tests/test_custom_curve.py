import unittest
from sage.all import ZZ, GF 
from curve_analyzer.utils.custom_curve import twisted_edwards_to_short_weierstrass, twisted_edwards_to_montgomery
#Test vectors: https://tools.ietf.org/id/draft-struik-lwip-curve-representations-00.html#rfc.appendix.C.3

p = 2 ** 255-19
F = GF(p)
a = -1
d = F(-121665)/(121666)
x = 15112221349535400772501151409588531511454012693041857206046113283949847762202
y = F(4)/(5)

Wei25519 = {'a': 19298681539552699237261830834781317975544997444273427339909597334573241639236,
            'b': 55751746669818908907645289078257140818241103727901012315294400837956729358436,
            'x': 19298681539552699237261830834781317975544997444273427339909597334652188435546,
            'y': 14781619447589544791020593568409986887264606134616475288964881837755586237401}

Mon25519 = {'A': 486662,
            'B': 1,
            'u': 9,
            'v': 14781619447589544791020593568409986887264606134616475288964881837755586237401
            }

class Test_custom_curve(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
    print("Everything passed")