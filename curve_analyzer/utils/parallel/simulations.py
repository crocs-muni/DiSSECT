import hashlib
from sage.all import *
import time

# hex string to binary string
def sha1_bin(x):
    return format(ZZ(hashlib.sha1(bytes.fromhex(x)).hexdigest(), 16), '0160b')


def sha1_hex(x):
    return format(ZZ(sha1(x), 2), '0160x')


def int_to_hex_string(x):
    f = '0' + str(ceil(x.nbits() / 8) * 2) + 'X'
    return format(ZZ(x, 16), f)


def increment_seed(seed, i=1):
    f = '0' + str(ceil(x.nbits() / 8) * 2) + 'X'
    return format(ZZ(x, 16), f)


def increment_seed(seed, i=1):
    '''accepts a hex string as input (not starting with 0x)'''
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
    #     print("t:",t, "s:", s, "h:", h)
    H = sha1_bin(seed)
    c0 = H[-h:]
    c0_modified = list(c0)
    c0_modified[0] = '0'
    W = [0] * (s + 1)
    W[0] = ''.join(c0_modified)
    for i in range(1, s+1):
        input_i = increment_seed(seed, i)
        W[i] = sha1_bin(input_i)
    W_joint = ''.join(W)
    assert (len(W_joint) == t)
    r = 0
    for i in range(1, t+1):
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


def has_root(pol, p):
    R = PolynomialRing(GF(p), 'x')
    S = R.quotient(pol, 'a')
    f1 = S(x)
    res = S(1)
    for bit in p.bits():
        if bit == 1:
            res *= f1
        f1 = S(f1 ** 2)
    return gcd(pol, res.lift() - x).degree() > 0


def has_points_of_low_order(E, l_max=4, poly_method='division'):
    assert poly_method in ['division', 'modular']
    p = E.base_field().order()
    R = PolynomialRing(GF(p), 'x')
    x = R.gen()

    if poly_method == 'modular':  # non-deterministic method
        mdb = ClassicalModularPolynomialDatabase()
        for l in prime_range(l_max):
            j = E.j_invariant()
            pol = R(mdb[l](j, x))
            if has_root(pol, p):
                return True
            else:
                continue

    if poly_method == 'division':  # deterministic method, useful for 256 bits with l_max = 4
        weier = x ** 3 + x * E.ainvs()[-2] + E.ainvs()[-1]
        for l in prime_range(l_max):
            #             print("l:", l)
            #             t1 = time.time()
            div_pol = E.division_polynomial(l)
            roots = div_pol.roots(GF(p))
            t2 = time.time()
            #             print("Div pol + roots computation:", t2-t1)
            for root, mult in roots:
                #                 t3 = time.time()
                issqr = weier(R(root)).is_square()
                #                 t4 = time.time()
                #                 print("Issqr:", issqr, t4-t3)
                if issqr:
                    return True
                else:
                    continue
    return False


def millerrabinliar(n, a):
    r = 0
    m = n - 1
    while m % 2 == 0:
        r += 1
        m = m / 2
    if Mod(a, n) ** m == Mod(1, n):
        return True
    for i in range(r):
        if Mod(a, n) ** (m * 2 ** i) == Mod(-1, n):
            return True
    return False


def millerrabin(n):
    for a in prime_range(200):
        if not millerrabinliar(n, a):
            return False
    return True


# A2.2 in http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.202.2977&rep=rep1&type=pdf
def verify_near_primality(u, r_min, l_max=255, MR=True):
    n = u
    h = 1
    for l in prime_range(l_max):
        while n % l == 0:
            n = ZZ(n / l)
            h = h * l
            if n < r_min:
                return (False, None, None)
    if MR and millerrabin(n):
        return (True, h, n)
    elif is_pseudoprime(n):
        return (True, h, n)
    return (False, None, None)


def verify_security(E, r_min_bits=160, B=20, MR=True, verbose=False):
    if verbose:
        print("Computing order")
    q = E.base_field().order()
    r_min = max(2 ** r_min_bits, 4 * sqrt(q))
    o = E.order()
    if verbose:
        print("Checking near-primality of", o)
    alright, h, n = verify_near_primality(o, r_min, MR=MR)
    if not alright:
        return (False, None, None)
    if verbose:
        print("Checking MOV")
    if embedding_degree(E, o) < B:
        return (False, None, None)
    if verbose:
        print("Checking Frob")
    if E.trace_of_frobenius() in [-1, 1]:
        return (False, None, None)
    return (True, h, n)

def embedding_degree(E, o):
    '''returns embedding degree with respect to q'''
    q = E.base_field().order()
    R = Integers(o)
    return R(q).multiplicative_order()

def generate_x962_curves(count, p, curve_seed, seed_offset=0, increment_step=1, fixed_a=True, verify=True,
                         r_min_bits=160, jsonfile="curves_json/x962-sim/curves.json",
                         logfile="curves_json/x962-sim/curves.log", MR=True, overwrite=False, verbosity_freq=1000,
                         l_max=20):
    assert fixed_a
    a = -3

    seed = increment_seed(curve_seed, seed_offset)
    bits = p.nbits()
    sim_curves = {}
    sim_curves["name"] = "x962_sim_" + str(bits)
    sim_curves["desc"] = "simulated curves generated according to the X9.62 standard"
    sim_curves["initial_seed"] = str(seed)
    sim_curves["seed_offset"] = str(seed_offset)
    sim_curves["curves_tried"] = count
    sim_curves["curves"] = []

    rel_seed = 0
    start_time = time.time()
    total_time = 0
    for i in range(1, count + 1):
        rel_seed = increment_step * i
        if i % verbosity_freq == 0:
            end_time = time.time()
            diff_time = end_time - start_time
            total_time += diff_time
            start_time = time.time()
        seed_i = increment_seed(seed, increment_step * i)
        r = generate_r(seed_i, p)
        b = get_b_from_r(r, p)
        if b == None:
            continue
        E = EllipticCurve(GF(p), [a, b])

        #         t1 = time.time()
        has_points = has_points_of_low_order(E, l_max, poly_method='division')
        #         t2 = time.time()
        #         print(t2-t1)
        if has_points:
            continue

        alright, h, n = verify_security(E, r_min_bits, MR=MR)
        if alright:
            assert h * n == E.order()
            sim_curve = {
                "name": "x962_sim_" + str(bits) + "_rel_seed_" + str(rel_seed),
                "category": sim_curves["name"],
                "desc": "",
                "field": {
                    "type": "Prime",
                    "p": str(hex(p)),
                    "bits": bits,
                },
                "form": "Weierstrass",
                "params": {
                    "a": str(hex(-3)),
                    "b": str(hex(b))
                },
                "generator": None,
                "order": n,
                "cofactor": h,
                "characteristics": None,
                "seed": seed_i
            }
            sim_curves["curves"].append(sim_curve)

    end_time = time.time()
    diff_time = end_time - start_time
    total_time += diff_time
    sim_curves["curves_total"] = len(sim_curves["curves"])
    sim_curves["total_time"] = total_time
    return sim_curves
