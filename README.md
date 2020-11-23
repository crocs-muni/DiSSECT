# Curve analyzer

[![pipeline status](https://gitlab.fi.muni.cz/x408178/curve_analyzer/badges/master/pipeline.svg)](https://gitlab.fi.muni.cz/x408178/curve_analyzer/-/commits/master)

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
   a01    | group_stucture_in_extensions                   | :heavy_check_mark: | :x:                | high         | low
   a02    | cm_disc_factorizations                         | :heavy_check_mark: | :x:                | high         | medium
   a04    | near_order_factorizations                      | :heavy_check_mark: | :x:                | high         | high
   a05    | torsion_extensions                             | :heavy_check_mark: | :heavy_check_mark: | medium       | low
   a06    | prime_decomposition_wrt_cm_discs_in_extensions | :heavy_check_mark: | :heavy_check_mark: | high         | medium
   a12    | orders_of_small_primes_modulo_curve_order      | :heavy_check_mark: | :heavy_check_mark: | medium       | medium
   a22    | division_pol_factorizations                    | :heavy_check_mark: | :white_check_mark: | high         | high
   a23    | volcano                                        | :heavy_check_mark: | :heavy_check_mark: | high         | low
   a24    | isogeny_extensions                             | :heavy_check_mark: | :white_check_mark: | medium       | low
   a25    | trace_factorization                            | :heavy_check_mark: | :heavy_check_mark: | low          | low
   i07    | distance_of_order_from_power_of_two            | :heavy_check_mark: | :white_check_mark: | low          | low

\* on sim and std curves with at most 256 bits  
\*\* this is very rough and subjective  
\*\*\* on the above dataset: low is  <100 MB, medium is 100-500 MB, high is >500 MB (measuring JSONs)

## Overview of all planned tests

## Unit tests
Run `sage --python3 -m unittest discover` in directory `tests/unit_tests/`.