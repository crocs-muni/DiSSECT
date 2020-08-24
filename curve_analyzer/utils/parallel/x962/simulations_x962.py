import json
from hashlib import sha1

from sage.all import ZZ, floor, ceil, GF, is_prime, PolynomialRing, EllipticCurve, prime_range, is_pseudoprime, \
    sqrt


# hex string to binary string
def sha1_bin(x):
    return format(ZZ(sha1(bytes.fromhex(x)).hexdigest(), 16), '0160b')


def sha1_hex(x):
    return format(ZZ(sha1(x), 2), '0160x')


def int_to_hex_string(x):
    f = '0' + str(ceil(x.nbits() / 8) * 2) + 'X'
    return format(ZZ(x, 16), f)


def increment_seed(seed, i=1):
    """accepts a hex string as input (not starting with 0x)"""
    g = ZZ(seed, 16).nbits()
    f = '0' + str(len(seed)) + 'X'
    return format(ZZ(Mod(ZZ(seed, 16) + i, 2 ** g)), f)


# http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.202.2977&rep=rep1&type=pdf, page 42
def generate_r(seed, p):
    t = p.nbits()
    #     t = ceil(log(p,2))
    #     originally floor
    s = floor((t - 1) / 160)
    h = t - 160 * s
    H = sha1_bin(seed)
    c0 = H[-h:]
    c0_modified = list(c0)
    c0_modified[0] = '0'
    W = [0] * (s + 1)
    W[0] = ''.join(c0_modified)
    for i in range(1, s + 1):
        input_i = increment_seed(seed, i)
        W[i] = sha1_bin(input_i)
    W_joint = ''.join(W)
    assert (len(W_joint) == t)
    r = 0
    for i in range(1, t + 1):
        r += ZZ(W_joint[i - 1]) * 2 ** (t - i)
    assert (r == ZZ(W_joint, 2))
    F = GF(p)
    return F(r)


def expected_r(p, a, b):
    F = GF(p)
    return F(a ** 3 / b ** 2)


def verify_r(p, r, a, b):
    F = GF(p)
    return F(r) == expected_r(p, a, b)


def get_b_from_r(r, p, a=-3):
    F = GF(p)
    if F(a ** 3 / r).is_square():
        return ZZ(F(a ** 3 / r).sqrt())
    else:
        return None


def embedding_degree_q(q, r):
    """returns embedding degree with respect to q"""
    return Mod(q, r).multiplicative_order()


def embedding_degree(E, r):
    """returns relative embedding degree with respect to E"""
    q = (E.base_field()).order()
    assert is_prime(q)
    return embedding_degree_q(q, r)


def has_points_of_low_order(E, l_max=4):
    # deterministic method utilizing division polynomials, useful for 256 bit E with l_max = 4 (see docs/division_early_abort)
    p = E.base_field().order()
    R = PolynomialRing(GF(p), 'x')
    x = R.gen()
    weier = x ** 3 + x * E.ainvs()[-2] + E.ainvs()[-1]
    for l in prime_range(l_max):
        div_pol = E.division_polynomial(l)
        roots = div_pol.roots(GF(p))
        for root, mult in roots:
            if weier(R(root)).is_square():
                return True
            else:
                continue
    return False


# A2.2 in http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.202.2977&rep=rep1&type=pdf
def verify_near_primality(u, r_min, l_max=255):
    n = u
    h = 1
    for l in prime_range(l_max):
        while n % l == 0:
            n = ZZ(n / l)
            h = h * l
            if n < r_min:
                return False, None, None
    if is_pseudoprime(n):
        return True, h, n
    return False, None, None


def verify_security(E, embedding_degree_bound=20, verbose=False):
    if verbose:
        print("Computing order")
    q = E.base_field().order()
    order = E.order()
    # a somewhat arbitrary bound (slightly more strict than in the standard), but it will speed up the generation process
    r_min_bits = order.nbits() - 5
    r_min = max(2 ** r_min_bits, 4 * sqrt(q))
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
    return True, h, n


def generate_x962_curves(count, p, seed):
    bits = p.nbits()
    sim_curves = {"name": "x962_sim_" + str(bits), "desc": "simulated curves generated according to the X9.62 standard",
                  "initial_seed": seed, "seeds_tried": count, "curves": [], "seeds_successful": 0}

    # bitlens, primes and corresponding seeds, case a=-3 (curves r1, prime fields only)
    # https://www.secg.org/sec2-v2.pdf
    with open('x962/parameters_x962.json', 'r') as f:
        params = json.load(f)
        original_seed = params[str(bits)][1]

    for i in range(1, count + 1):
        current_seed = increment_seed(seed, -i)
        r = generate_r(current_seed, p)
        b = get_b_from_r(r, p)
        a = -3

        # check if r gives rise to an elliptic curve
        if b is None or 4 * a ** 3 + 27 * b ** 2 == 0:
            continue
        E = EllipticCurve(GF(p), [a, b])

        # a heuristic for speeding up the generation process in exchange for sacrificing some curves with low cofactor
        if bits < 224:
            l_max = 3
            if bits < 192:
                l_max = 2
        else:
            l_max = 4
        if has_points_of_low_order(E, l_max):
            continue

        secure, h, n = verify_security(E)
        if not secure:
            continue

        seed_diff = ZZ('0X' + original_seed) - ZZ('0X' + current_seed)
        sim_curve = {
            "name": "x962_sim_" + str(bits) + "_seed_diff_" + str(seed_diff),
            "category": sim_curves["name"],
            "desc": "",
            "field": {
                "type": "Prime",
                "p": str(hex(p)),
                "bits": bits,
            },
            "form": "Weierstrass",
            "params": {
                "a": {"raw": str(hex(-3))},
                "b": {"raw": str(hex(b))}
            },
            "generator": {
                "x": {
                    "raw": ""
                },
                "y": {
                    "raw": ""
                }
            },
            "order": n,
            "cofactor": h,
            "characteristics": None,
            "seed": current_seed,
            "seed_diff": seed_diff
        }
        sim_curves["curves"].append(sim_curve)
        sim_curves["seeds_successful"] += 1

    return sim_curves
