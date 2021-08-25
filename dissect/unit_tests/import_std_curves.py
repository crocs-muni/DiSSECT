import unittest

from dissect.utils.curve_handler import import_curves


class TestImportStdCurves(unittest.TestCase):
    def test_import_sample(self):
        curves = import_curves(
            curve_type="sample", order_bound=256, allowed_cofactors=[1]
        )
        self.assertEqual(len(curves), 3)

        curves = import_curves(
            curve_type="sample", order_bound=256, allowed_cofactors=[2, 3, 4, 5]
        )
        self.assertEqual(len(curves), 0)

    def test_import_std(self):
        curves = import_curves(curve_type="std", order_bound=113, allowed_cofactors=[1])
        self.assertEqual(len(curves), 3)

        curves = import_curves(curve_type="std", order_bound=113, allowed_cofactors=[4])
        self.assertEqual(len(curves), 1)

        curves = import_curves(
            curve_type="std", order_bound=113, allowed_cofactors=[1, 4]
        )
        self.assertEqual(len(curves), 4)


if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
