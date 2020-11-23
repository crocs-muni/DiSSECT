# Curve analyzer

[![pipeline status](https://gitlab.fi.muni.cz/x408178/curve_analyzer/badges/master/pipeline.svg)](https://gitlab.fi.muni.cz/x408178/curve_analyzer/-/commits/master)

# Setup

Run `sage --python3 setup.py develop`.

## Unit tests
Run `sage --python3 -m unittest discover` in directory `tests/unit_tests/`.

## Generating structure files
Run `tests_structures.py -t all` in directory `tests`.

## Testing the curves

Run `./run_tests.py` in directory `tests`. Use the `-h` flag to get the help menu. To merge the results of a test (a22 in this case) into single file, run `./merge_test_results.py -n a22`.

### Example usage

To run test a22 on all standard curves of bitsizes up to 192 in verbose mode using 3 cores and 100 jobs, run `./run_tests.py -n a22 -c std -v -b 192 -t 3 -j 100`.

### Supported curve sets

- std: all standard curves
- sim: all simulated curves
- sample: curves secp112r1, secp192r1, secp256r1
- all: all curves in the database

### Overview of available tests

| name | description	| implemented  	|  computed\* 	|  time req. 	| memory req.  	|
|---	|---	|---	|---	|---	|---	|
a01 | group_stucture_in_extensions 					 | yes | no 	| high | low
a02 | cm_disc_factorizations						 | yes | no 	| high | low
a04 | near_order_factorizations 					 | yes | no 	| high | low
a05 | torsion_extensions 							 | yes | yes 	| medium | low
a06 | prime_decomposition_wrt_cm_discs_in_extensions | yes | yes 	| high | medium
a12 | orders_of_small_primes_modulo_curve_order		 | yes | yes 	| medium | low
a22 | division_pol_factorizations					 | yes | partly | high | high
a23 | volcano										 | yes | yes 	| high | low
a24 | isogeny_extensions							 | yes | partly | medium | low
a25 | trace_factorization							 | yes | yes 	| low | low
i07 | distance_of_order_from_power_of_two			 | yes | partly | low  | low

\*on curves with at most 256 bits

### Overview of all planned tests