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

**Full DiSSECT installation**:
- Clone with  `git clone --recurse-submodules https://github.com/crocs-muni/DiSSECT.git`
- Create virtual environment for Python in Sage: `sage --python3 -m venv --system-site-packages environment`
- Activate the environment: `source environment/bin/activate`
- Run `pip install --editable .` in DiSSECT folder

**DiSSECT without Sage (only analysis)**:
- Clone with  `git clone --recurse-submodules https://github.com/crocs-muni/DiSSECT.git`
- Create virtual environment for Python: `python -m venv environment`
- Activate the environment: `source environment/bin/activate`
- Run `pip install --editable .` in DiSSECT folder

# Commands

## Computing traits

To feed the trait results directly to a local MongoDB database, run `dissect-compute-database`. Alternatively, to get results as a JSON files, run `dissect-compute-file`. Use the `-h` flag to get the help menu.

## Performing the analysis

The visual analysis can be started directly from local dissect installation by running `jupyter notebook` in DiSSECT root directory. Alternatively, the analysis framework can be started directly in the browser with Binder service.

In order to run outlier detection, feature vectors need to be constructed. They can be built from results of individual traits using repeated invocations of `dissect-feature_builder`. For example, the following sequence of commands builds set of feature vectors of `torsion_extension` and `small_prime_order` traits for 256-bit curves from the standard and simulated X9.62 categories.

```
dissect-feature_builder --trait torsion_extension --category x962 x962_sim --bits 256 --input out.csv --output out.csv
dissect-feature_builder --trait small_prime_order --category x962 x962_sim --bits 256 --input out.csv --output out.csv
```

The sequence of `dissect-feature_builder` runs produces file `out.csv`, which contains the resulting feature vectors. The feature vectors can processed by the outlier detection script `dissect-find_outliers`.

```
dissect-find_outliers out.csv outliers.csv
```

## Importing curves or results to a database

After setting up a local database with MongoDB, you can run `dissect-database curves [database_uri] <curve_files...>` to import curves from individual JSON files. Similarly, you can run `dissect-database results [database_uri] <trait_name> <results_file>` to import trait results from a JSON file.
