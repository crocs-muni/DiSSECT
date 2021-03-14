import ast
import unittest

from dissect.traits.example_curves import curve_names
from dissect.traits.i06.i06 import i06_curve_function

results = {
    "secp112r2": {"{}": {"p": 1, "order": 1}},
    "bn158": {"{}": {"p": 5, "order": 277}},
    "brainpoolP160r1": {"{}": {"p": 627, "order": 3}},
}


class TestI06(unittest.TestCase):
    def test_auto_generated_secp112r2(self):
        """This test has been auto-generated by gen_unittest"""
        params = ast.literal_eval(list(results["secp112r2"].keys())[0]).values()
        computed_result = i06_curve_function(curve_names["secp112r2"], *params)
        self.assertEqual(list(results["secp112r2"].values())[0], computed_result)

    def test_auto_generated_bn158(self):
        """This test has been auto-generated by gen_unittest"""
        params = ast.literal_eval(list(results["bn158"].keys())[0]).values()
        computed_result = i06_curve_function(curve_names["bn158"], *params)
        self.assertEqual(list(results["bn158"].values())[0], computed_result)

    def test_auto_generated_brainpoolP160r1(self):
        """This test has been auto-generated by gen_unittest"""
        params = ast.literal_eval(list(results["brainpoolP160r1"].keys())[0]).values()
        computed_result = i06_curve_function(curve_names["brainpoolP160r1"], *params)
        self.assertEqual(list(results["brainpoolP160r1"].values())[0], computed_result)


if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
