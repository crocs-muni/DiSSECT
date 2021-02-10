import unittest, ast
from dissect.traits.a05.a05 import a05_curve_function
from dissect.traits.example_curves import curves, curve_names
results={'secp112r2': {"{'l': 2}": {'least': 1, 'full': 2, 'relative': 2}}, 'bn158': {"{'l': 2}": {'least': 3, 'full': 3, 'relative': 1}}, 'brainpoolP160r1': {"{'l': 2}": {'least': 3, 'full': 3, 'relative': 1}}}

class TestA05(unittest.TestCase):
 
    def test_auto_generated_secp112r2(self):
        """This test has been auto-generated by gen_unittest""" 
        params = ast.literal_eval(list(results["secp112r2"].keys())[0]).values()
        computed_result = a05_curve_function(curve_names["secp112r2"],*params)
        self.assertEqual(computed_result,list(results["secp112r2"].values())[0])

    def test_auto_generated_bn158(self):
        """This test has been auto-generated by gen_unittest""" 
        params = ast.literal_eval(list(results["bn158"].keys())[0]).values()
        computed_result = a05_curve_function(curve_names["bn158"],*params)
        self.assertEqual(computed_result,list(results["bn158"].values())[0])

    def test_auto_generated_brainpoolP160r1(self):
        """This test has been auto-generated by gen_unittest""" 
        params = ast.literal_eval(list(results["brainpoolP160r1"].keys())[0]).values()
        computed_result = a05_curve_function(curve_names["brainpoolP160r1"],*params)
        self.assertEqual(computed_result,list(results["brainpoolP160r1"].values())[0])


if __name__ == '__main__':
   unittest.main()
   print("Everything passed")
