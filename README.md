# DiSSECT: Distinguisher of Standard & Simulated Elliptic Curves via Traits

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://gitlab.fi.muni.cz/x408178/curve_analyzer/-/blob/master/LICENSE)
[![language](https://badgen.net/badge/language/python,sage/purple?list=/)](https://www.sagemath.org/)
[![traits](https://badgen.net/badge/traits/23/blue)](https://github.com/crocs-muni/DiSSECT/tree/master/dissect/traits)
[![Binder](https://static.mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/crocs-muni/DiSSECT/master)

DiSSECT is, to the best of our knowledge, the largest publicly available database of standardized elliptic curves (taken from our [sister project](https://neuromancer.sk/std/)) and offers generation of simulated curves according to the mentioned standards. The tool contains over 20 tests (which we call traits), each computing curve properties, ranging from classical algebraic ones to unconventional ones and those connected to implementations. After obtaining their empirical distributions, the traits allow us to compare the simulated curves to the standard ones. Finally, DiSSECT provides an easy-to-use interface for implementations of custom traits and their interactive visualization via Jupyter notebook.

DiSSECT is written in Python 3 and imports the SageMath library. The database of the standardized elliptic curves as well as the simulated ones with the results of the traits, including the visualization, can be found at https://dissect.crocs.fi.muni.cz/. DiSSECT is open-source and we welcome any collaborators who have an idea for a new trait, new simulation method, or just want to contribute in another way.

### Authors

- Vladimír Sedláček
- Vojtěch Suchánek
- Antonín Dufka

Thanks to Ján Jančár for help with the curve database and CRoCS members for fruitful discussions. Computational resources were supplied by the project "e-Infrastruktura CZ" (e-INFRA LM2018140) provided within the program Projects of Large Research, Development and Innovations Infrastructures.

# Running DiSSECT

We highly recommend using DiSSECT in Docker, as it avoids potential issues on the boundary of Sage and Python environments. If you still want to run DiSSECT locally, see the Local setup section.

## Docker

Clone this repository and build docker image.

```shell
$ git clone --recurse-submodules https://github.com/crocs-muni/DiSSECT
$ cd DiSSECT
$ docker build -t dissect .
```

When the image is successfully built, you can start using DiSSECT.

To run Jupyter Notebook, use the following command and access the provided link in your web browser.

```
docker run -it -p 8888:8888 dissect jupyter notebook dissect/analysis --ip='0.0.0.0' --port=8888
```

To run other DiSSECT commands in the Docker container, prefix them with `docker run -i dissect`. For example, `docker run -i dissect dissect-compute-file`. Alternatively, you can access DiSSECT directly in the container by opening interactive shell `docker run -it dissect bash`.

## Local setup

**Using virtual environment**:

- Clone with  `git clone --recurse-submodules https://github.com/crocs-muni/DiSSECT.git`
- Create virtual environment for python in sage: `sage --python3 -m venv --system-site-packages environment`
- Activate the environment: `source environment/bin/activate`
- Run `pip install --editable .` in DiSSECT folder

**Alternatively without virtual environment (not recommended)**:
From the root directory, run `sage --python3 setup.py develop --user` to initialize the project.

# Commands

## Computing traits

To feed the trait results directly to a local MongoDB database, run `dissect-compute-database`. Alternatively, to get results as a JSON files, run `dissect-compute-file`. Use the `-h` flag to get the help menu.

## Performing the analysis

The visual analysis can be started directly from local dissect installation by running `jupyter notebook` in DiSSECT root directory. Alternatively, the analysis framework can be started directly in the browser with Binder service.

In order to run outlier detection, feature vectors need to be constructed. They can be built from results of individual traits using repeated invocations of `dissect-feature_builder`. For example, the following sequence of commands builds set of feature vectors of `a05` and `a12` traits for 256-bit curves from the standard and simulated X9.62 categories.

```
dissect-feature_builder --trait a05 --category x962 x962_sim --bits 256 --input out.csv --output out.csv
dissect-feature_builder --trait a12 --category x962 x962_sim --bits 256 --input out.csv --output out.csv
```

The sequence of `dissect-feature_builder` runs produces file `out.csv`, which contains the resulting feature vectors. The feature vectors can processed by the outlier detection script `dissect-find_outliers`.

```
dissect-find_outliers out.csv outliers.csv
```

## Overview of available traits

| name    | description                                                                       | implemented        |  computed\*        |time req.\*\* |memory req.\*\*\*
|:-------:| ----------------------------------------------------------------------------------|:------------------:|:------------------:|:------------:|:---------:   
|a01      | group stucture of the curve in field extensions                                   | :white_check_mark: | :x:                | high         | low
|a02      | factorization of the CM discriminant                                              | :white_check_mark: | :white_check_mark: | high         | medium
|a03      | factorization of the quadratic twist cardinality                                  | :white_check_mark: | :white_check_mark: | high         | medium
|a04      | factorizations of $`kn\pm 1`$                                                     | :white_check_mark: | :white_check_mark: | high         | high
|a05      | field extensions containing nontrivial/full $`l`$-torsion                         | :white_check_mark: | :white_check_mark: | medium       | low
|a06      | factorizations of ratios of CM discriminants in extension fields and base fields  | :white_check_mark: | :white_check_mark: | high         | medium
|a07      | embedding degree                                                                  | :white_check_mark: | :white_check_mark: | medium       | low
|a08      | class number of the maximal order of the endomorphism ring                        | :white_check_mark: | :white_check_mark:               | high         | low
|a12      | multiplicative orders of small primes modulo curve order                          | :white_check_mark: | :white_check_mark: | medium       | medium
|a22      | factorizations of small division polynomials                                      | :white_check_mark: | :white_check_mark: | high         | high
|a23      | volcano depth and crater degree in the $`l`$-isogeny graph                        | :white_check_mark: | :white_check_mark: | low          | low
|a24      | field extensions containing nontrivial/full number of $`l`$-isogenies             | :white_check_mark: | :white_check_mark: | medium       | low
|a25      | trace in field extensions and its factorization                                   | :white_check_mark: | :white_check_mark: | low          | low
|a28      | Number of j-invariants adjacent to the curve by l-isogeny                         |:white_check_mark:|:white_check_mark:| medium | low
|a29      |Torsion order of the lift of E to curve over Q                                     |:white_check_mark:|:white_check_mark:|low | low
|i04      | number of points with low Hamming weight                                          | :white_check_mark: | :white_check_mark: | medium       | low
|i06      | square parts of $`4q-1`$ and $`4n-1`$                                             | :white_check_mark: | :white_check_mark: | low          | low
|i07      | distance of $`n`$ from the nearest power of two and multiple of 32/64             | :white_check_mark: | :white_check_mark: | low          | low
|i08      | bit length of small inverted generator multiples                                  | :white_check_mark: | :white_check_mark: | low          | low
|i13      |$` a^3/b^2`$, i.e. value used in x962, fips,secg                                       | :white_check_mark: | :white_check_mark:                | low          | low
|i14      | overlap in curve coefficients                                       | :white_check_mark: | :white_check_mark:                | low          | low
|i15      | curve coefficients in Weierstrass form                                       | :white_check_mark: | :white_check_mark:                | low          | low


Notation: $`n`$ is the curve order, $`q`$ is the order of the base field  
\* on sim and std curves with at most 256 bits and cofactor 1    
\*\* this is very rough and subjective  
\*\*\* on the above dataset: low is  <100 MB, medium is 100-500 MB, high is >500 MB (measuring JSONs)

## Overview of planned traits

| name    | description                                                                       | fully specified
|:-------:| ----------------------------------------------------------------------------------|:------------------:
a09       | existence of pairing-friendly cycles                                              | :x:
a10       | existence of factorization bases                                                  | :x:
a11       | minimal codewords in elliptic codes                                               | :x:
a13       | images of points under pairings                                                   | :x:
a14       | conductor and modularity                                                          | :x:
a15       | the lattice associated to the curve over $`C`$                                    | :x:
a16       | the Neron model                                                                   | :x:
a17       | the L-series                                                                      | :x:
a18       | the invariant differential                                                        | :x:
a19       | local heights                                                                     | :x:
a20       | $`S`$-integral points                                                             | :x:
a21       | Galois groups of various polynomials                                              | :x:
a26       | lifts of curves to other fields                                                   | :x:
a27       | distribution and sizes of isogeny classes                                         | :x:
i01       | curves under parameter bitflips                                                   | :x:
i02       | curves with the same $`j`$-invariant/group order, but different $`q`$             | :x:
i03       | the number of modular reductions in various computations                          | :x:
i05       | vulnerability against $`\rho`$ and kangaroo                                       | :x:
s01       | statistical properties of scalar multiplication                                   | :x:
s02       | distribution of point coordinates in various intervals                            | :x:
s03       | properties of other curve models                                                  | :x:
s04       | modular polynomials in given $`j`$-invariant                                      | :x:
s05       | images of points under isogenies                                                  | :x:
s06       | summation polynomials                                                             | :x:
s07       | distributions of curves with similar properties                                   | :x:
s08       | properties of the function shifting a point by the generator                      | :x:

## Unit tests

Run `sage --python3 -m unittest discover` in directory `traits/unit_tests/`. Only unit tests starting with `test` will be run; those starting with `local` have to be run manually (as they require resources not available on the server).

## Importing curves or results to a database

After setting up a local database with MongoDB, you can run `dissect-database curves [database_uri] <curve_files...>` to import curves from individual JSON files. Similarly, you can run `dissect-database results [database_uri] <trait_name> <results_file>` to import trait results from a JSON file.
