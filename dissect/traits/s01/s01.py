from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve
from sage.all import ZZ, RR, sqrt, variance,std
from hashlib import sha1

def hamm(weight, bit_length):
    val = 2 ** weight - 1
    hams = []
    while val.bit_length() <= bit_length:
        hams.append(val)
        c = val & -val
        r = val + c
        val = (((r ^ val) >> 2) // c) | r
    return hams


COMB_L = 6
HAMM = {i: hamm(i, 256) for i in [1, 2]}


def random_point(curve, seed=0):
    gen = curve.generator()
    i = seed
    dgst = sha1(i.to_bytes(3, byteorder='big')).digest()
    scalar = int.from_bytes(dgst, byteorder='big') % curve.q()
    return scalar * gen, curve.order() // scalar.gcd(curve.order())


def statistics(mean1, mean2, mean3, mean4, stat1, stat2, Hamm_length):
    values = {'Arithmetic mean': arithmetic_mean(mean1, Hamm_length),
              'Geometric mean': geometric_mean(mean2, Hamm_length,True),
              'Quadratic mean': quadratic_mean(mean3, Hamm_length), 'Harmonic mean': harmonic_mean(mean4, Hamm_length),
              'Variance': float(variance(stat1)), 'Standard deviation': float(std(stat2, False))}

    return values


def arithmetic_mean(num, constant):
    return float(num / constant)


def quadratic_mean(num, constant):
    return float((sqrt(num / constant)))


def geometric_mean(num, constant,convert = False):
    gm = RR(num).nth_root(constant)
    gm = float(gm) if convert else gm
    return gm


def harmonic_mean(num, constant):
    return float(constant / num)


def s01_curve_function(curve: CustomCurve, weight):
    if curve.generator() is None:
        P, n = random_point(curve)
    else:
        P, n = curve.generator(), curve.order()
    final_arithmetic_mean = 0
    final_geometric_mean = 1
    final_quadratic_mean = 0
    final_harmonic_mean = 0

    stat_variance = []
    stat_std = []
    for i in HAMM[weight]:
        Q = int(i) * P
        a = n / 2
        b = n / 2
        starting_point = int(a) * P + int(b) * Q
        quadratic_num = 0
        geometric_num = 1
        final_sum = 0
        harmonic_num = 0
        stat_lst = []
        for _ in range(2 ** COMB_L - 1):
            if ZZ(starting_point[0]) < n / 4:
                starting_point = 2 * P + starting_point
                a = (a + 2) % n
                b = b % n
            elif n / 4 <= ZZ(starting_point[0]) < n / 2:
                starting_point = P + starting_point
                a = (a + 1) % n
                b = b % n
            elif n / 2 <= ZZ(starting_point[0]) < 3 * (n / 4):
                starting_point = Q + starting_point
                a = a % n
                b = (b + 1) % n
            else:
                starting_point = 2 * Q + starting_point
                a = a % n
                b = (b + 2) % n
            value = (ZZ(starting_point[0])).nbits() if (ZZ(starting_point[0])).nbits() != 0 else 1
            final_sum = final_sum + value
            geometric_num = geometric_num * value
            quadratic_num = quadratic_num + (ZZ(starting_point[0]) ** 2).nbits()
            harmonic_num = harmonic_num + 1 / (value)
            stat_lst.append((ZZ(starting_point[0])).nbits())
        final_arithmetic_mean += arithmetic_mean(final_sum, 2 ** COMB_L)
        final_geometric_mean = final_geometric_mean * geometric_mean(geometric_num, 2 ** COMB_L)
        final_quadratic_mean += (quadratic_mean(quadratic_num, 2 ** COMB_L)) ** 2
        final_harmonic_mean += 1 / (harmonic_mean(harmonic_num, 2 ** COMB_L))
        stat_variance.append(variance(stat_lst))
        stat_std.append(std(stat_lst, False))
    return statistics(final_arithmetic_mean, final_geometric_mean, final_quadratic_mean, final_harmonic_mean,
                      stat_variance, stat_std, len(HAMM[weight]))


def compute_s01_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "s01", s01_curve_function, desc=desc, verbose=verbose)
