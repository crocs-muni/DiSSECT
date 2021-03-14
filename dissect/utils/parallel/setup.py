from setuptools import find_packages
from setuptools import setup

version = "0.0.0"

# Please update tox.ini when modifying dependency version requirements
install_requires = [
    "sarge",
    "psutil",
    "pid>=2.0.1",
    "coloredlogs",
    "shellescape",
]

dev_extras = [
    "nose",
    "pep8",
    "tox",
]

docs_extras = [
    "Sphinx>=1.0",  # autodoc_member_order = 'bysource', autodoc_default_flags
    "sphinx_rtd_theme",
    "sphinxcontrib-programoutput",
]

setup(
    name="parallel_curve_analyser",
    version=version,
    description="Parallel execution",
    url="https://github.com/crocs-muni/Parallel_Curve_analyser",
    author="CRoCS",
    author_email="xsvenda@fi.muni.cz",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Security",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        "dev": dev_extras,
        "docs": docs_extras,
    },
)
