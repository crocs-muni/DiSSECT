from sage.all import GF, ZZ
from dissect.utils.curve_form import dict_to_poly, CurveForm
import unittest

# sect163k1
BINARY_MODULUS = dict_to_poly([{"power": 163, "coeff": "0x01"}, {"power": 7, "coeff": "0x01"},
                               {"power": 6, "coeff": "0x01"}, {"power": 3, "coeff": "0x01"},
                               {"power": 0, "coeff": "0x01"}, ], GF(2)["w"])
BINARY_FIELD = GF(2 ** 163, "w", BINARY_MODULUS, proof=False)
BINARY_CURVE = {"form": "weierstrass", "a": {"raw": "0x000000000000000000000000000000000000000001"},
                "b": {"raw": "0x000000000000000000000000000000000000000001"}}
BINARY_POINT = {"x": {"raw": "0x02fe13c0537bbc11acaa07d793de4e6d5e5c94eee8"},
                "y": {"raw": "0x0289070fb05d38ff58321f2e800536d538ccdaa3d9"}}

# Fp254n2BNa
EXTENSION_PRIME = ZZ(0x2370fb049d410fbe4e761a9886e502417d023f40180000017e80600000000001)
EXTENSION_MODULUS = dict_to_poly([{"power": 2, "coeff": "0x01"}, {"power": 0, "coeff": "0x05"}],
                                 GF(EXTENSION_PRIME)["w"])
EXTENSION_FIELD = GF(EXTENSION_PRIME ** 2, "w", EXTENSION_MODULUS, proof=False)
EXTENSION_CURVE = {"form": "weierstrass", "a": {"poly": [{"power": 0, "coeff": "0x00"}]}, "b": {
    "poly": [{"power": 1, "coeff": "0x2370fb049d410fbe4e761a9886e502417d023f40180000017e80600000000000"}]}}
EXTENSION_POINT = {"x": {
    "poly": [{"power": 1, "coeff": "0xa1cf585585a61c6e9880b1f2a5c539f7d906fff238fa6341e1de1a2e45c3f72"},
             {"power": 0, "coeff": "0x19b0bea4afe4c330da93cc3533da38a9f430b471c6f8a536e81962ed967909b5"}]}, "y": {
    "poly": [{"power": 1, "coeff": "0x0ee97d6de9902a27d00e952232a78700863bc9aa9be960C32f5bf9fd0a32d345"},
             {"power": 0, "coeff": "0x17abd366ebbd65333e49c711a80a0cf6d24adf1b9b3990eedcc91731384d2627"}]}}

# x962_sim_256_seed_diff_302361
WEIERSTRASS_FIELD = GF(ZZ(0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff))
WEIERSTRASS_CURVE = {"form": "weierstrass", "a": {"raw": "-0x3"},
                     "b": {"raw": "0x226c4993ea4df0010cfc11dbb66cbbfedb0ace35bf1f3020473c4bd94a2e339a"}}

# JubJub
EDWARDS_FIELD = GF(ZZ(0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001))
EDWARDS_CURVE = {"form": "edwards", "a": {"raw": "0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000000"},
                 "d": {"raw": "0x2a9318e74bfa2b48f5fd9207e6bd7fd4292d7f6d37579d2601065fd6d6343eb1"}}
EDWARDS_POINT = {"x": {"raw": "0x11dafe5d23e1218086a365b99fbf3d3be72f6afd7d1f72623e6b071492d1122b"},
                 "y": {"raw": "0x1d523cf1ddab1a1793132e78c866c0c33e26ba5cc220fed7cc3f870e59d292aa"}}

# M-221
MONTGOMERY_FIELD = GF(ZZ(0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD))
MONTGOMERY_CURVE = {"form": "montgomery", "a": {"raw": "0x01c93a"}, "b": {"raw": "0x01"}}
MONTGOMERY_POINT = {"x": {"raw": "0x04"}, "y": {"raw": "0x0f7acdd2a4939571d1cef14eca37c228e61dbff10707dc6c08c5056d"}}


class TestCustomCurve(unittest.TestCase):
    def test_binary(self):
        form = CurveForm(BINARY_FIELD, BINARY_CURVE)
        self.assertEqual(form.a().integer_representation(), 1)
        self.assertEqual(form.b().integer_representation(), 1)
        point = form.point(BINARY_POINT['x'], BINARY_POINT['y'])
        self.assertEqual(point[0].integer_representation(), 4373527398576640063579304354969275615843559206632)
        self.assertEqual(point[1].integer_representation(), 3705292482178961271312284701371585420180764402649)

    def test_extension(self):
        form = CurveForm(EXTENSION_FIELD, EXTENSION_CURVE)
        a, b = dict_to_poly(EXTENSION_CURVE['a']["poly"], EXTENSION_FIELD), dict_to_poly(EXTENSION_CURVE['b']["poly"],
                                                                                         EXTENSION_FIELD)
        self.assertEqual(form.a(), a)
        self.assertEqual(form.b(), b)
        point = form.point(EXTENSION_POINT['x'], EXTENSION_POINT['y'])
        x, y = dict_to_poly(EXTENSION_POINT['x']["poly"], EXTENSION_FIELD), dict_to_poly(EXTENSION_POINT['y']["poly"],
                                                                                         EXTENSION_FIELD)
        self.assertEqual(point[0], x)
        self.assertEqual(point[1], y)

    def test_weierstrass(self):
        form = CurveForm(WEIERSTRASS_FIELD, WEIERSTRASS_CURVE)
        self.assertEqual(form.a(), -3)
        self.assertEqual(form.b(), 15569964150097736379485471556633208273069500795165954536126230123980599997338)

    def test_edwards(self):
        form = CurveForm(EDWARDS_FIELD, EDWARDS_CURVE)
        self.assertEqual(form._ea, 52435875175126190479447740508185965837690552500527637822603658699938581184512)
        self.assertEqual(form._ed, 19257038036680949359750312669786877991949435402254120286184196891950884077233)
        self.assertEqual(form._a, 52435875175126190479447740508185965837690552500527637822603658699938021889366)
        self.assertEqual(form._b, 5091077286874)
        point = form.point(EDWARDS_POINT['x'], EDWARDS_POINT['y'])
        self.assertEqual(point[0], 37380265172535953876205871964221324158436172047572074969815349807835370919958)
        self.assertEqual(point[1], 26380167486300012236235446069573518237842295555935462158915317449484086642989)

    def test_montgomery(self):
        form = CurveForm(MONTGOMERY_FIELD, MONTGOMERY_CURVE)
        self.assertEqual(form._ma, 117050)
        self.assertEqual(form._mb, 1)
        self.assertEqual(form._a,2246662222262553316222251257251635889469762035211714373420733953267)
        self.assertEqual(form._b, 2371476790166028500456820771543393438884748814945698624072426982903)
        point = form.point(MONTGOMERY_POINT['x'],MONTGOMERY_POINT['y'])
        self.assertEqual(point[0], 2246662222262553316222251257251635889469762035211714373425300893120)
        self.assertEqual(point[1], 1630203008552496124843674615123983630541969261591546559209027208557)


if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
