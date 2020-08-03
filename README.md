# Curve analyzer

[![pipeline status](https://gitlab.fi.muni.cz/x408178/curve_analyzer/badges/master/pipeline.svg)](https://gitlab.fi.muni.cz/x408178/curve_analyzer/-/commits/master)

# Setup

Run `sage --python3 setup.py develop`.

## Unit tests

Run `sage --python3 -m unittest discover` in directory `tests/unit_tests/`.

## Testing the curves

Run `./run_tests.py` in directory `tests`. Use the `-h` flag to get the help menu.

### Example usage

To run test a22 on standard curves of bitsizes up to 192 in verbose mode, run `./run_tests.py a22 std -v -b 192`.

### Supported curve sets

- std: all standard curves
- sim: all simulated curves
- sample: curves secp112r1, secp192r1, secp256r1
- all: all curves in the database

### Overview of available tests

- a02_cm_disc_factorizations
- a04_near_order_factorizations
- a05_torsion_extensions
- a12_orders_of_small_primes_modulo_curve_order
- a22_division_pol_factorizations
- a23_volcano
- a24_isogeny_extensions
- a25_trace_factorization
