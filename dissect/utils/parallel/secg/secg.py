"""This is an implementation of the SEC standard, see
    https://www.secg.org/sec2-v2.pdf
    https://www.secg.org/sec1-v2.pdf
    Only cofactor=1 is implemented. SHA-1 is used.
    A=-3 is forced
"""

import json
from hashlib import sha1

from sage.all import (
    Integers,
    ZZ,
    floor,
    ceil,
    GF,
    is_prime,
    Integer,
    EllipticCurve,
    prime_range,
    is_pseudoprime,
    sqrt,
)

N_PM_1_TEST = False  # Flag for testing the condition on the size of prime divisors of n+/-1 (see the SEC 1 standard)


def sha1_bin(x):
    """ Returns sha1 hash of x in 160bit binary """
    return format(ZZ(sha1(bytes.fromhex(x)).hexdigest(), 16), "0160b")


def sha1_hex(x):
    """Returns sha1 hash of x in 160bit hex"""
    return format(ZZ(sha1(x), 2), "0160x")


def int_to_hex_string(x):
    """Converts int to hex string"""
    f = "0" + str(ceil(x.nbits() / 8) * 2) + "X"
    return format(ZZ(x, 16), f)


def increment_seed(seed, i=1):
    """accepts a hex string as input (not starting with 0x)"""
    g = ZZ(seed, 16).nbits()
    f = "0" + str(len(seed)) + "X"
    return format(ZZ(Integers(2 ** g)(ZZ(seed, 16) + i)), f)


def generate_r(seed, p):
    """Generates r where r*b^2=a^3 (see the standard)"""
    t = p.nbits()
    s = floor((t - 1) / 160)
    h = t - 160 * s
    H = sha1_bin(seed)
    c0 = H[-h:]
    c0_modified = list(c0)
    c0_modified[0] = "0"
    W = [0] * (s + 1)
    W[0] = "".join(c0_modified)
    for i in range(1, s + 1):
        input_i = increment_seed(seed, i)
        W[i] = sha1_bin(input_i)
    W_joint = "".join(W)
    assert len(W_joint) == t
    r = 0
    for i in range(1, t + 1):
        r += ZZ(W_joint[i - 1]) * 2 ** (t - i)
    assert r == ZZ(W_joint, 2)
    F = GF(p)
    return F(r)


def get_b_from_r(r, p, a=-3):
    """computes b from r*b^2=a^3 given r and a"""
    F = GF(p)
    if F(a ** 3 / r).is_square():
        return ZZ(F(a ** 3 / r).sqrt())
    else:
        return None


def embedding_degree_q(q, r):
    """returns embedding degree with respect to q"""
    return Integers(r)(q).multiplicative_order()


def embedding_degree(E, r):
    """returns relative embedding degree with respect to E"""
    q = (E.base_field()).order()
    assert is_prime(q)
    return embedding_degree_q(q, r)


def verify_near_primality(u, r_min, l_max=255):
    """Find the cofactor h and factor n where n*h=u is the cardinality of the curve"""
    n = u
    h = 1
    for l in prime_range(58, l_max):  # 58 is the start as smaller primes are tested during ellsea computation
        while n % l == 0:
            n = ZZ(n / l)
            h = h * l
            if n < r_min:
                return False, None, None
    if is_pseudoprime(n):
        return True, h, n
    return False, None, None


def n_1_test(n, m, lower_bound=19 / 20):
    """
    Tests the size of the largest prime divisor of m (m = n-1 or n+1)
    This test is used iff the flag N_PM_1 is True
    """
    bound = floor(n ** (1 - lower_bound))
    h, l = Integer(1), Integer(2)
    tmp = m
    while h < bound and l < bound:
        if tmp % l == 0:
            h *= l
            tmp = tmp // l
            continue
        l = l.next_prime()
    if h >= bound:
        return False
    if tmp.is_prime():
        return True
    return False


def cofactor_size(cofactor, p):
    """Tests the size of cofactor"""
    t = {192: 80, 512: 256}.get(p.nbits(), p.nbits() // 2)
    return cofactor <= 2 ** (t / 8)


def verify_security(E, p, embedding_degree_bound=100, verbose=False):
    order = E.__pari__().ellsea(1)
    if order == 0:
        return False, None, None
    order = Integer(order)
    # an arbitrary bound (slightly more strict than in the standard), but it will speed up the generation process
    r_min_bits = order.nbits() - 5
    r_min = max(2 ** r_min_bits, 4 * sqrt(p))
    if verbose:
        print("Checking near-primality of", order)
    near_prime, h, n = verify_near_primality(order, r_min)
    if not near_prime:
        return False, None, None
    if verbose:
        print("Checking MOV")
    if embedding_degree(E, order) < embedding_degree_bound:
        return False, None, None
    if verbose:
        print("Checking Frob")
    if E.trace_of_frobenius() in [-1, 1]:
        return False, None, None
    if N_PM_1_TEST and not (n_1_test(n, n - 1) and n_1_test(n, n + 1)):
        return False, None, None
    if not cofactor_size(h, p):
        return False, None, None
    return True, h, n


def gen_point(seed, p, E, h):
    """Returns generator as specified in SEC"""
    A = bytearray("Base point", 'ASCII')
    B = bytearray.fromhex("01")
    S = bytearray.fromhex(seed)
    c = Integer(1)
    while True:
        C = bytearray.fromhex(int_to_hex_string(c))
        R = A
        for byte in [B, C, S]:
            R.extend(byte)
        e = ZZ(sha1(R).hexdigest(), 16)
        t = e % (2 * p)
        x, z = t % p, t // p
        c += 1
        try:
            y = E.lift_x(x)[1]
        except ValueError:
            continue
        if Integer(y) % 2 == z:
            return E(x, y) * h


def gen_curve(p, seed, b_sign=False):
    """
    Generates SEC curve over F_p out of 160bit seed
    The b_sign argument is to force (when True) that both roots of r*x^2=a^3 are tested for b.
     - This is mainly for testing.
    """
    r = generate_r(seed, p)
    b = get_b_from_r(r, p)
    a = -3
    if b is None or 4 * a ** 3 + 27 * b ** 2 == 0:
        return None

    E = EllipticCurve(GF(p), [a, b])
    secure, h, n = verify_security(E, p)
    if not secure:
        if not b_sign or p % 4 == 1:
            return None
        E = EllipticCurve(GF(p), [a, -b])
        secure, h, n = verify_security(E, p)
        if not secure:
            return None
    return E, gen_point(seed, p, E, h), n


def test_gen_curve():
    """Testing of gen_curve on standardized SEC curves"""
    with open("testing_parameters_secg.json", "r") as file:
        secg = json.load(file)
    for name, curve_dict in secg.items():
        nbits = Integer(nbits[4:-2])
        print(nbits)
        res = gen_curve(ZZ(curve_dict['p'], 16), curve_dict['seed'], b_sign=True)
        assert res is not None
        curve, P, n = res
        p = curve.base_field().order()
        assert int_to_hex_string(Integer(curve.a4())) == curve_dict['A']
        B = Integer(curve.a6())
        assert int_to_hex_string(B) == curve_dict['B'] or int_to_hex_string(p - B) == curve_dict['B']
        assert int_to_hex_string(p) == curve_dict['p']
