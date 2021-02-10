import unittest, ast
from dissect.traits.a23.a23 import a23_curve_function
from dissect.traits.example_curves import curves, curve_names
results={'secp112r2': {"{'l': 2}": {'crater_degree': 0, 'depth': 1}}, 'bn158': {"{'l': 2}": {'crater_degree': 0, 'depth': 0}}, 'brainpoolP160r1': {"{'l': 2}": {'crater_degree': 0, 'depth': 0}}}

class TestA23(unittest.TestCase):
 
    def test_auto_generated_secp112r2(self):
        """This test has been auto-generated by gen_unittest""" 
        params = ast.literal_eval(list(results["secp112r2"].keys())[0]).values()
        computed_result = a23_curve_function(curve_names["secp112r2"],*params)
        self.assertEqual(list(results["secp112r2"].values())[0],computed_result)

    def test_auto_generated_bn158(self):
        """This test has been auto-generated by gen_unittest""" 
        params = ast.literal_eval(list(results["bn158"].keys())[0]).values()
        computed_result = a23_curve_function(curve_names["bn158"],*params)
        self.assertEqual(list(results["bn158"].values())[0],computed_result)

    def test_auto_generated_brainpoolP160r1(self):
        """This test has been auto-generated by gen_unittest""" 
        params = ast.literal_eval(list(results["brainpoolP160r1"].keys())[0]).values()
        computed_result = a23_curve_function(curve_names["brainpoolP160r1"],*params)
        self.assertEqual(list(results["brainpoolP160r1"].values())[0],computed_result)


if __name__ == '__main__':
   unittest.main()
   print("Everything passed")
