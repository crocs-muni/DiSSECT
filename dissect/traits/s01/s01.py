#!/usr/bin/env python3

from sage.all import variance

from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve


def custom_points(E, number=10000):
    points = []
    for _ in range(number):
        points.append(E.random_point())
    return points


def histogram_x(E, n):
    prime = E.base_field().order()
    sort = sorted(custom_points(E))
    counter = 0
    i = 1
    results = []
    for P in sort:
        if (float(P[0]) >= (i - 1) * (prime / n)) and (float(P[0]) <= i * (prime / n)):
            counter += 1
        else:
            results.append(counter)
            i += 1
            counter = 1
    results.append(counter)
    return results


def s01_curve_function(curve: CustomCurve):
    E = curve.EC
    hist = histogram_x(E, 10)
    curve_results = {"histogram": hist, "value": variance(hist)}
    return curve_results


def compute_s01_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "s01", s01_curve_function, desc=desc, verbose=verbose)
