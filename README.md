# Curve analyzer

[![pipeline status](https://gitlab.fi.muni.cz/x408178/curve_analyzer/badges/master/pipeline.svg)](https://gitlab.fi.muni.cz/x408178/curve_analyzer/-/commits/master)

# Setup

Run `sage --python3 setup.py develop`.

## Unit tests

Run `sage --python3 -m unittest discover` in the tests/unit_tests/ directory.

## Testing the curves

Run `./run_tests.py` from the test directory.

### Example usage

To run test a22 on standard curves of bitsizes up to 192 in verbose mode, run `./run_tests.py a22 std -v -b 192`.