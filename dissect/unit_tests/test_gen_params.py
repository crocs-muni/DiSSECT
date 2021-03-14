import json
import os
import pathlib
import unittest

import dissect.traits.gen_params as g
from dissect.definitions import TRAIT_PATH


class TestGenParams(unittest.TestCase):
    def test_read(self):
        result = g.read_default(pathlib.Path(TRAIT_PATH, "default.params"))
        for test in result:
            self.assertIn(
                "params_global", result[test], "Wrong format of parameters for " + test
            )
            self.assertIn(
                "params_local_names",
                result[test],
                "Wrong format of parameters for " + test,
            )
        if "i07" in result:
            self.assertEqual(
                result["i07"]["params_global"],
                {},
                "Wrong global params for i07, should be " + "{}",
            )
            self.assertEqual(
                result["i07"]["params_local_names"],
                [],
                "Wrong local params for i07, should be " + "[]",
            )

    def test_write_i07(self):
        i07tmp = "i07.params"
        result = g.read_default(pathlib.Path(TRAIT_PATH, "default.params"))
        g.write_file("i07", i07tmp, result["i07"], "")
        shouldbe = {"params_global": {}, "params_local_names": []}
        with open(i07tmp, "r") as f:
            self.assertDictEqual(
                json.load(f), shouldbe, "Wrong param generation for i07"
            )
        os.remove(i07tmp)


if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
