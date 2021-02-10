import unittest

from dissect.utils.curve_handler import import_curves


class TestImportSimCurves(unittest.TestCase):
    def test_import_sim(self):
        curves = import_curves(curve_type="sim", order_bound=128, allowed_cofactors=[1])
        self.assertEqual(len(curves), 15916)

        curves = import_curves(curve_type="sim", order_bound=128, allowed_cofactors=list(range(1, 1001)))
        self.assertEqual(len(curves), 93796)


if __name__ == '__main__':
    unittest.main()
    print("Everything passed")
