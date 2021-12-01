import itertools
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve
from sage.all import ZZ, RR, sqrt
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

HAMM = {i: hamm(i, 256) for i in [1, 2, 3]}


def scenario_1(starting_point, P, Q, a, b, n):
    starting_point = 2 * P + starting_point
    a = (a + 2) % n
    b = b % n
    return starting_point, P, Q, a, b, n


def scenario_2(starting_point, P, Q, a, b, n):
    starting_point = P + starting_point
    a = (a + 1) % n
    b = b % n
    return starting_point, P, Q, a, b, n


def scenario_3(starting_point, P, Q, a, b, n):
    starting_point = Q + starting_point
    a = a % n
    b = (b + 1) % n
    return starting_point, P, Q, a, b, n


def scenario_4(starting_point, P, Q, a, b, n):
    starting_point = 2 * Q + starting_point
    a = a % n
    b = (b + 2) % n
    return starting_point, P, Q, a, b, n


def random_point(curve, seed=0):
    gen = curve.generator()
    i = seed
    dgst = sha1(i.to_bytes(3, byteorder='big')).digest()
    scalar = int.from_bytes(dgst, byteorder='big') % curve.q()
    return scalar * gen, curve.order() // scalar.gcd(curve.order())


functions = (scenario_1, scenario_2, scenario_3, scenario_4)


def means(num1, num2, num3, num4):
    return {'Arithmetic mean': arithmetic_mean(num1), 'Geometric mean': geometric_mean(num2),
            'Quadratic mean': quadratic_mean(num3), 'Harmonic mean': harmonic_mean(num4)}


def arithmetic_mean(num):
    return float(num / (2 ** 10))


def quadratic_mean(num):
    return float((sqrt(num / (2 ** 10))))


def geometric_mean(num):
    return RR(num).n().nth_root(2 ** 10)


def harmonic_mean(num):
    return float((2 ** 10) / num)


def s01_curve_function(curve: CustomCurve, current_combination, weight):
    P, n = random_point(curve)
    n = P.order()
    final_arithmetic_mean = 0
    final_geometric_mean = 1
    final_quadratic_mean = 0
    final_harmonic_mean = 0

    permutations = list(itertools.permutations([0, 1, 2, 3]))
    for i in HAMM[weight]:
        Q = int(i) * P
        a = n / 2
        b = n / 2
        starting_point = int(a) * P + int(b) * Q
        quadratic_num = 0
        geometric_num = 1
        final_sum = 0
        harmonic_num = 0
        for _ in range(2 ** 10 - 1):
            if ZZ(starting_point[0]) < n / 4:
                starting_point, P, Q, a, b, n = functions[permutations[current_combination][0]](starting_point, P, Q, a,
                                                                                                b, n)
            elif n / 4 <= ZZ(starting_point[0]) < n / 2:
                starting_point, P, Q, a, b, n = functions[permutations[current_combination][1]](starting_point, P, Q, a,
                                                                                                b, n)
            elif n / 2 <= ZZ(starting_point[0]) < 3 * (n / 4):
                starting_point, P, Q, a, b, n = functions[permutations[current_combination][2]](starting_point, P, Q, a,
                                                                                                b, n)
            else:
                starting_point, P, Q, a, b, n = functions[permutations[current_combination][3]](starting_point, P, Q, a,
                                                                                                b, n)
            final_sum = final_sum + (ZZ(starting_point[0])).nbits()
            geometric_num = geometric_num * (ZZ(starting_point[0])).nbits()
            quadratic_num = quadratic_num + (ZZ(starting_point[0]) ** 2).nbits()
            harmonic_num = harmonic_num + 1 / ((ZZ(starting_point[0])).nbits() + 1)
        final_arithmetic_mean += arithmetic_mean(final_sum)
        final_geometric_mean = final_geometric_mean * geometric_mean(geometric_num)
        final_quadratic_mean += quadratic_mean(quadratic_num) ** 2
        final_harmonic_mean += 1 / (harmonic_mean(harmonic_num))
    return means(final_arithmetic_mean, final_geometric_mean, final_quadratic_mean, final_harmonic_mean)


def compute_s01_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "s01", s01_curve_function, desc=desc, verbose=verbose)
