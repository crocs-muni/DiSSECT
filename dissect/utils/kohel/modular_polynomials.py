"""
Modified code from SageMath db_modular_polynomials.py by William Stein,
David Kohel, Vincent Delecroix
"""
# ****************************************************************************
#       Copyright (C) 2006 William Stein <wstein@gmail.com>
#       Copyright (C) 2006 David Kohel <kohel@maths.usyd.edu.au>
#       Copyright (C) 2016 Vincent Delecroix <vincent.delecroix@labri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************
import bz2
import os
from sage.cpython.string import bytes_to_str
from sage.all import Integer, IntegerRing, PolynomialRing
import importlib.resources


def modular_polynomials(level):
    try:
        with importlib.resources.files("dissect.utils.kohel").joinpath(
            "mod", f"pol.{level:03d}.dbz"
        ).open("rb") as f:
            data = bz2.decompress(f.read())
    except IOError:
        raise ValueError("file not found in the Kohel database")
    data = bytes_to_str(data)
    coeff_list = [
        [Integer(v) for v in row.strip().split(" ")] for row in data.split("\n")[:-1]
    ]
    P = PolynomialRing(IntegerRing(), 2, "j")
    poly = {}
    if level == 1:
        return P({(1, 0): 1, (0, 1): -1})
    for cff in coeff_list:
        i = cff[0]
        j = cff[1]
        poly[(i, j)] = Integer(cff[2])
        if i != j:
            poly[(j, i)] = Integer(cff[2])
    return P(poly)
