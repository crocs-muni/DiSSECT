# DiSSECT: Distinguisher of Standard & Simulated Elliptic Curves via Traits

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://gitlab.fi.muni.cz/x408178/curve_analyzer/-/blob/master/LICENSE)
[![language](https://badgen.net/badge/language/python,sage/purple?list=/)](https://www.sagemath.org/)
[![traits](https://badgen.net/badge/traits/23/blue)](https://github.com/crocs-muni/DiSSECT/tree/master/dissect/traits)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crocs-muni/DiSSECT/blob/master/dissect/analysis/playground.ipynb#offline=1)

DiSSECT is, to the best of our knowledge, the largest publicly available database of standardized elliptic curves (taken from our [sister project](https://neuromancer.sk/std/)) and offers generation of simulated curves according to the mentioned standards. The tool contains over 20 tests (which we call traits), each computing curve properties, ranging from classical algebraic ones to unconventional ones and those connected to implementations. After obtaining their empirical distributions, the traits allow us to compare the simulated curves to the standard ones. Finally, DiSSECT provides an easy-to-use interface for implementations of custom traits and their interactive visualization via Jupyter notebook.

DiSSECT is written in Python 3 and imports the SageMath library. The database of the standardized elliptic curves as well as the simulated ones with the results of the traits, including the visualization, can be found at https://dissect.crocs.fi.muni.cz/. DiSSECT is open-source and we welcome any collaborators who have an idea for a new trait, new simulation method, or just want to contribute in another way.

### Authors

- Vladimír Sedláček
- Vojtěch Suchánek
- Antonín Dufka

Thanks to Ján Jančár for help with the curve database and CRoCS members for fruitful discussions. Computational resources were supplied by the project "e-Infrastruktura CZ" (e-INFRA LM2018140) provided within the program Projects of Large Research, Development and Innovations Infrastructures.

# Installation

We recommend to use DiSSECT in Docker, as it avoids potential issues on the boundary of Sage and Python environments. If you still want to run DiSSECT locally, see the [Local setup](#local-setup) section.

## Docker container

Clone this repository and build docker image.

```shell
git clone --recurse-submodules https://github.com/crocs-muni/DiSSECT
cd DiSSECT
docker build -t dissect .
```

When the image is successfully built, you can start using DiSSECT.

To run Jupyter Notebook, use the following command and access the provided link in your web browser.

```shell
docker run -it -p 8888:8888 dissect
```

To use advanced components of DiSSECT, access the container directly.

## Local setup

### Full (requires `sage`)

If you plan on computing traits, you need to perform full instalation of DiSSECT using Sage.

```shell
git clone --recurse-submodules https://github.com/crocs-muni/DiSSECT.git
cd DiSSECT
sage --python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install .
python -m ipykernel install --user --name=venv
jupyter notebook dissect/analysis/playground.ipynb
```

### Analysis-only

If you only need to access DiSSECT database, inspect the data, and perform analyses, Python-based installation will suffice.

```shell
git clone --recurse-submodules https://github.com/crocs-muni/DiSSECT.git
cd DiSSECT
python -m venv venv
source venv/bin/activate
pip install .
python -m ipykernel install --user --name=venv
jupyter notebook dissect/analysis/playground.ipynb
```

# Commands

To run these commands, you need a working installation of DiSSECT – either in an interactive container or a local one. If you plan to share files between host and the docker container, you may want to use a [bind mount](https://docs.docker.com/storage/bind-mounts/) (e.g., `--mount type=bind,src=/tmp/dissect,dst=/data`).

## Computing traits

DiSSECT provides two ways of computing traits: a simple one suitable for working with just JSON files, and more complex one that supports parallelization but requires database, intended mainly for large-scale trait computation.

To compute traits on a JSON of curves, use:
```shell
dissect-compute-json -t TRAIT_NAME -i CURVES_JSON [-o OUTPUT_JSON]
```

To compute traits with database, use:
```shell
dissect-compute-db -t TRAIT_NAME --database DATABASE_URL
```
By default, the command uses all available curves. You can filter them using optional arguments, see the help menu (`-h`).

## Performing the analysis

To run analysis notebook, use the following command and select the `venv` kernel.
```
jupyter notebook dissect/analysis/playground.ipynb
```
Alternatively, you may try using the notebook directly in your browser using [Colab](https://colab.research.google.com/github/crocs-muni/DiSSECT/blob/master/dissect/analysis/playground.ipynb#offline=1).

### Automated analysis

In order to run automated analysis of trait results, feature vectors need to be constructed. They can be built from results of individual traits using repeated invocations of `dissect-feature_builder`. For example, the following sequence of commands builds set of feature vectors of `torsion_extension` and `small_prime_order` traits for 256-bit curves from the standard and simulated X9.62 categories.
```shell
dissect-feature_builder --trait torsion_extension --category x962 x962_sim --bits 256 --input features.csv --output features.csv
dissect-feature_builder --trait small_prime_order --category x962 x962_sim --bits 256 --input features.csv --output features.csv
```
By default, this command uses a dataset available from our database, but you may supply a different source using the `--source` option (url to a database).

The feature vectors output by the previous commands can be processed by the outlier detection script:
```shell
dissect-feature_outliers features.csv outliers.csv
```

If the outlier detection gave an interesting output, you may inspect features of a particular curve with:
```shell
dissect-feature_detail features.csv CURVE_NAME
```

Another approach to automated analysis implemented in DiSSECT is clustering. Clustering requires feature vectors curves of two distinct categories and running `feature_builder` with `--keep-category` option. Then, it can be run as:
```shell
dissect-feature_clusters features.csv outliers.csv
```

## Database

Command `dissect-database` provides a simple interface for uploading DiSSECT data from JSON files to a database for further analysis. To use this command you have to provide database URL which should be a string in format `"mongodb://USERNAME:PASSWORD@HOST/"` (e.g., `"mongodb://root:password@mongo:27017/`).

To upload curves from a JSON file, use:
```shell
dissect-database curves [DATABASE_URL] <CURVE_FILES...>
```

To upload trait results from a JSON file, use:
```shell
dissect-database traits [DATABASE_URL] <TRAIT_NAME> <TRAIT_RESULTS_FILE>
```