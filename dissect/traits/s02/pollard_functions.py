from sage.all import ZZ, sqrt, std, variance, RR
import random

def hams(weight, bit_length):
    val = 2 ** weight - 1
    hams_list = []
    while val.bit_length() <= bit_length:
        hams_list.append(val)
        c = val & -val
        r = val + c
        val = (((r ^ val) >> 2) // c) | r
    return hams_list


def random_hams(n, weight, bit_length, seed):
    l = hams(weight, bit_length)
    final_lst = []
    for _ in range(n):
        random.seed(seed)
        rand = random.choice(l)
        final_lst.append(rand)
    return final_lst


SEED = 1
N = 100
RANDOM_HAMS_2 = random_hams(100, 2, 256, SEED)
HAMS_1 = hams(1, 256)


def generator(curve, seed=1):
    while True:
        random.seed(seed)
        x = random.randint(0, curve.q())
        try:
            gen = curve.ec().lift_x(curve.field()(x))
        except ValueError:
            seed += 1
            continue
        gen = (curve.cardinality() // curve.order()) * gen
        if gen == curve.ec()(0):
            seed += 1
            continue
        return gen


def pollard(curve, hamming_weight, option, num_of_inner_cycles):
    if curve.generator() is None:
        P = generator(curve)
    else:
        P = curve.generator()
    n = curve.order()

    final_arithmetic_mean = 0
    final_geometric_mean = 1
    final_quadratic_mean = 0
    final_harmonic_mean = 0
    num_of_subgroups = 20
    if hamming_weight == 1:
        list_of_k = HAMS_1
    else:
        list_of_k = RANDOM_HAMS_2
    ham_length = len(list_of_k)
    stat_variance = []
    stat_std = []
    for i in list_of_k:
        Q = int(i) * P
        a = n / 2
        b = n / 2
        starting_point = int(a) * P + int(b) * Q
        quadratic_num = 0
        geometric_num = 1
        final_sum = 0
        harmonic_num = 0
        stat_lst = []
        for _ in range(num_of_inner_cycles):
            a, b, starting_point = choose_function(option, a, b, starting_point, n, P, Q, num_of_subgroups)

            value = (ZZ(starting_point[0])).nbits() if (ZZ(starting_point[0])).nbits() != 0 else 256
            final_sum = final_sum + value
            geometric_num = geometric_num * value
            quadratic_num = quadratic_num + value ** 2
            harmonic_num = harmonic_num + 1 / value
            stat_lst.append(value)

        final_arithmetic_mean += arithmetic_mean(final_sum, num_of_inner_cycles)
        final_geometric_mean = final_geometric_mean * geometric_mean(geometric_num, num_of_inner_cycles)
        final_quadratic_mean += (quadratic_mean(quadratic_num, num_of_inner_cycles)) ** 2
        final_harmonic_mean += 1 / (harmonic_mean(harmonic_num, num_of_inner_cycles))
        stat_variance.append(variance(stat_lst))
        stat_std.append(std(stat_lst, False))
    return statistics(final_arithmetic_mean, final_geometric_mean, final_quadratic_mean, final_harmonic_mean,
                      stat_variance, stat_std, ham_length)


def choose_function(option, a, b, starting_point, n, P, Q, num_of_subgroups):
    if option == 1:  # Pollard Original Walk (1-4)
        if ZZ(starting_point[0]) < n / 4:
            starting_point = 2 * P + starting_point
            a = (a + 2) % n
            b = b % n
            return a, b, starting_point
        elif n / 4 <= ZZ(starting_point[0]) < n / 2:
            starting_point = P + starting_point
            a = (a + 1) % n
            b = b % n
            return a, b, starting_point
        elif n / 2 <= ZZ(starting_point[0]) < 3 * (n / 4):
            starting_point = Q + starting_point
            a = a % n
            b = (b + 1) % n
            return a, b, starting_point
        else:
            starting_point = 2 * Q + starting_point
            a = a % n
            b = (b + 2) % n
            return a, b, starting_point

    if option == 2:  # Pollard Original Walk (1-16, 1-2, 15-16)
        if ZZ(starting_point[0]) < n / 16:
            starting_point = 2 * P + starting_point
            a = (a + 2) % n
            b = b % n
            return a, b, starting_point
        elif n / 16 <= ZZ(starting_point[0]) < n / 2:
            starting_point = P + starting_point
            a = (a + 1) % n
            b = b % n
            return a, b, starting_point
        elif n / 2 <= ZZ(starting_point[0]) < 15 * (n / 16):
            starting_point = Q + starting_point
            a = a % n
            b = (b + 1) % n
            return a, b, starting_point
        else:
            starting_point = 2 * Q + starting_point
            a = a % n
            b = (b + 2) % n
            return a, b, starting_point

    if option == 3:  # Pollard Original Walk (1-3)
        if ZZ(starting_point[0]) < n / 3:
            starting_point = P + starting_point
            a = (a + 1) % n
            b = b % n
            return a, b, starting_point
        elif n / 3 <= ZZ(starting_point[0]) < 2 * (n / 3):
            starting_point = 2 * starting_point
            a = (2 * a) % n
            b = (2 * b) % n
            return a, b, starting_point
        else:
            starting_point = Q + starting_point
            a = a % n
            b = (b + 1) % n
            return a, b, starting_point

    if option == 4:  # Pollard Adding Walk
        return eval_comp_adding(num_of_subgroups, n, starting_point, P, Q, a, b)

    if option == 5:  # Pollard Mixed Walk
        return eval_comp_mixed(num_of_subgroups, n, starting_point, P, Q, a, b)

    else:
        return eval_comp_modified(num_of_subgroups, n, starting_point, P, Q, a, b)


def eval_function(num_of_subgroups, R):
    A = (sqrt(5) - 1) / 2
    B = A.n(digits=10)
    val = float(float(B) * int(R[1])) % 1
    return int(val * num_of_subgroups) + 1


def eval_comp_adding(num_of_subgroups, n, R, P, Q, a, b):
    list_A = []
    list_B = []
    for _ in range(num_of_subgroups):
        list_A.append(random.randint(1, n))
        list_B.append(random.randint(1, n))
    pos = eval_function(num_of_subgroups, R)
    R = R + list_A[pos - 1] * P + list_B[pos - 1] * Q
    a = (a + list_A[pos - 1]) % n
    b = (b + list_B[pos - 1]) % n
    return a, b, R


def eval_comp_mixed(num_of_subgroups, n, R, P, Q, a, b):
    list_A = []
    list_B = []
    exception_classes = []
    while len(exception_classes) < 4:  # creates a list with 4 classes where different operation of R will be held
        E = random.randint(1, 20)
        if E not in exception_classes:
            exception_classes.append(E)
    for _ in range(num_of_subgroups):
        list_A.append(random.randint(1, n))
        list_B.append(random.randint(1, n))
    pos = eval_function(num_of_subgroups, R)
    for _ in exception_classes:
        if pos in exception_classes:
            R = 2 * R
            a = 2 * a
            b = 2 * b
        else:
            R = R + list_A[pos - 1] * P + list_B[pos - 1] * Q
            a = (a + list_A[pos - 1]) % n
            b = (b + list_B[pos - 1]) % n
    return a, b, R


def eval_comp_modified(num_of_subgroups, n, R, P, Q, a, b):
    m = random.randint(1, n - 1)
    o = random.randint(1, n - 1)
    M, N = m * P, o * P
    pos = eval_function(num_of_subgroups, R)
    if pos == 1:
        R = M + R
        a = (int(a + m)) % n
    elif pos == 2:
        R = 2 * R
        a = 2 * a
        b = 2 * b
    else:
        R = N + R
        b = (int(a + o)) % n
    return a, b, R


def statistics(mean1, mean2, mean3, mean4, stat1, stat2, Hamm_length):
    values = {'Arithmetic mean': arithmetic_mean(mean1, Hamm_length),
              'Geometric mean': float(geometric_mean(mean2, Hamm_length)),
              'Quadratic mean': quadratic_mean(mean3, Hamm_length), 'Harmonic mean': harmonic_mean(mean4, Hamm_length),
              'Variance': float(variance(stat1)), 'Standard deviation': float(std(stat2, False))}

    return values


def arithmetic_mean(num, constant):
    return float(num / constant)


def quadratic_mean(num, constant):
    return float((sqrt(num / constant)))


def geometric_mean(num, constant):
    return RR(num).n().nth_root(constant)


def harmonic_mean(num, constant):
    return float(constant / num)

