# Curve analyzer

[![pipeline status](https://gitlab.fi.muni.cz/x408178/curve_analyzer/badges/master/pipeline.svg)](https://gitlab.fi.muni.cz/x408178/curve_analyzer/-/commits/master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://gitlab.fi.muni.cz/x408178/curve_analyzer/-/blob/master/LICENSE)
[![tests](https://badgen.net/badge/tests/13/blue)](https://gitlab.fi.muni.cz/x408178/curve_analyzer/-/tree/master/curve_analyzer/tests)
[![curves](https://badgen.net/badge/curves/158%20std,%20217188%20sim?list=|)](https://github.com/J08nY/std-curves)

# Setup

Run `sage --python3 setup.py develop` to initialize the project, then `sage --python3 params.py` to generate parameter files and `sage --python3 tests/tests_structures.py -t all` to generate structure files.

## Testing the curves

Run `./run_tests.py` in directory `tests`. Use the `-h` flag to get the help menu. To merge the results of a test (a22 in this case) into single file, run `./merge_test_results.py -n a22`.

### Example usage

To run test a22 on all standard curves of bitsizes up to 192 in verbose mode using 3 cores and 100 jobs, run `./run_tests.py -n a22 -c std -v -b 192 -t 3 -j 100`.

### Supported curve sets

- std: all standard curves
- sim: all simulated curves
- sample: curves secp112r1, secp192r1, secp256r1
- all: all curves in the database

## Overview of available tests

| name    | description                                    | implemented        |  computed\*        |time req.\*\* |memory req.\*\*\*
|:-------:| -----------------------------------------------|:------------------:|:------------------:|:------------:|:---------:   
   a01    | group_stucture_in_extensions                   | :white_check_mark: | :x:                | high         | low
   a02    | cm_disc_factorizations                         | :white_check_mark: | :x:                | high         | medium
   a04    | near_order_factorizations                      | :white_check_mark: | :x:                | high         | high
   a05    | torsion_extensions                             | :white_check_mark: | :white_check_mark: | medium       | low
   a06    | prime_decomposition_wrt_cm_discs_in_extensions | :white_check_mark: | :white_check_mark: | high         | medium
   a12    | orders_of_small_primes_modulo_curve_order      | :white_check_mark: | :white_check_mark: | medium       | medium
   a22    | division_pol_factorizations                    | :white_check_mark: | :soon:             | high         | high
   a23    | volcano                                        | :white_check_mark: | :white_check_mark: | high         | low
   a24    | isogeny_extensions                             | :white_check_mark: | :soon:             | medium       | low
   a25    | trace_factorization                            | :white_check_mark: | :white_check_mark: | low          | low
   i07    | distance_of_order_from_power_of_two            | :white_check_mark: | :soon:             | low          | low

\* on sim and std curves with at most 256 bits  
\*\* this is very rough and subjective  
\*\*\* on the above dataset: low is  <100 MB, medium is 100-500 MB, high is >500 MB (measuring JSONs)

## Overview of all planned tests

## Unit tests
Run `sage --python3 -m unittest discover` in directory `tests/unit_tests/`.
