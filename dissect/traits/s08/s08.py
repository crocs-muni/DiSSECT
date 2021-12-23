from sage.all import variance, std, ZZ, sqrt, RR
from dissect.utils.custom_curve import CustomCurve
from dissect.traits.trait_interface import compute_results
from dissect.traits.s02.pollard_functions import hams, random_hams, generator


SEED = 1
RANDOM_HAMS = {i:random_hams(2 ** 11, i, 256, SEED) for i in [2,3]}
HAMS_1 = hams(1, 256)


def scalar_multiplication(curve, Hamm_weight):
    if curve.generator() is None:
        P = generator(curve)
    else:
        P = curve.generator()
    n = curve.order()
    bit_length = n.nbits()

    stats = BasicStats()
    if Hamm_weight == 1:
        lst_of_scalars = HAMS_1
    else:
        lst_of_scalars = RANDOM_HAMS[Hamm_weight]
    means = Means(len(lst_of_scalars))

    for i in lst_of_scalars:
        Q = P * int(i)
        value = x_coord_bits(Q, bit_length)
        stats.append(value)
        means.update(value)
    means.finalize()
    var = stats.variance()
    std = stats.std()
    return statistics(means.arithmetic_mean.value, means.geometric_mean.value, means.quadratic_mean.value,
                      means.harmonic_mean.value, var, std)


def x_coord_bits(point, bit_length):
    return (ZZ(point[0])).nbits() if (ZZ(point[0])).nbits() != 0 else bit_length


def statistics(mean1, mean2, mean3, mean4, var, std):
    values = {'Arithmetic mean': mean1, 'Geometric mean': mean2, 'Quadratic mean': mean3, 'Harmonic mean': mean4,
              'Variance': var, 'Standard deviation': std}

    return values


class ArithmeticMean:
    def __init__(self, count):
        self.value = 0
        self.count = count

    def update(self, current_value):
        self.value += current_value

    def finalize(self):
        self.value = float(self.value / self.count)


class GeometricMean:
    def __init__(self, count):
        self.value = 1
        self.count = count

    def update(self, current_value):
        self.value *= current_value

    def finalize(self):
        self.value = float(RR(self.value).n().nth_root(self.count))


class QuadraticMean:
    def __init__(self, count):
        self.value = 0
        self.count = count

    def update(self, current_value):
        self.value += current_value ** 2

    def finalize(self):
        self.value = float(sqrt(self.value / self.count))


class HarmonicMean:
    def __init__(self, count):
        self.value = 0
        self.count = count

    def update(self, current_value):
        self.value += 1 / current_value

    def finalize(self):
        self.value = float(self.count / self.value)


class Means:
    def __init__(self, count):
        self.arithmetic_mean = ArithmeticMean(count)
        self.geometric_mean = GeometricMean(count)
        self.quadratic_mean = QuadraticMean(count)
        self.harmonic_mean = HarmonicMean(count)

    def update(self, value):
        self.arithmetic_mean.update(value)
        self.geometric_mean.update(value)
        self.quadratic_mean.update(value)
        self.harmonic_mean.update(value)

    def finalize(self):
        self.arithmetic_mean.finalize()
        self.geometric_mean.finalize()
        self.quadratic_mean.finalize()
        self.harmonic_mean.finalize()


class BasicStats:
    def __init__(self):
        self.values = []

    def append(self, value):
        self.values.append(value)

    def variance(self):
        return float(variance(self.values))

    def std(self):
        return float(std(self.values, False))


def s08_curve_function(curve: CustomCurve, weight):
    return scalar_multiplication(curve, weight)


def compute_s08_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "s08", s08_curve_function, desc=desc, verbose=verbose)
