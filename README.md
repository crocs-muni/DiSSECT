# Curve analysis

[![pipeline status](https://gitlab.fi.muni.cz/x408178/curve_analyzer/badges/master/pipeline.svg)](https://gitlab.fi.muni.cz/x408178/curve_analyzer/-/commits/master)

For setup, run

`sage --python3 setup.py develop`

For unit tests, run 

`sage --python3 -m unittest discover`

in the tests/unit_tests/ directory

For testing the curves, run `./run_tests.py` from the test directory.

Example usage: 

`./run_tests.py a22 std -v -b 192`

(runs test a22 on standard curves of bitsizes up to 192 in verbose mode)