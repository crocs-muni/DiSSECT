"""This is an implementation of the Brainpool standard, see
    https://tools.ietf.org/pdf/rfc5639.pdf#15
    https://web.archive.org/web/20180417212206/http://www.ecc-brainpool.org/download/Domain-parameters.pdf
"""

from sage.all import ceil, ZZ, floor, PolynomialRing, Integers, squarefree_part, BinaryQF, xsrange, gcd, lcm, randint, \
    GF, EllipticCurve, Integer
import hashlib
import json

CHECK_CLASS_NUMBER = False


def int_to_hex_string(x, prefix=False, lower_case=False):
    """Converts int to hex without prefix 0x, padded"""
    form = "x" if lower_case else "X"
    f = "0" + str(ceil(x.nbits() / 8) * 2) + form
    hex = format(ZZ(x, 16), f)
    if prefix:
        hex = "0" + form + hex
    return hex


def update_seed(s, i=1):
    """Increments 160bit seed by i"""
    z = ZZ(s, 16)
    return int_to_hex_string((z + i) % (2 ** 160))


def rightmost_bits(h, nbits):
    """Returns nbits of rightmost bits of h"""
    return int_to_hex_string(ZZ(h, 16) % (2 ** nbits))


def sha1(x):
    """Returns sha1 of x in hex"""
    return hashlib.sha1(bytes.fromhex(x)).hexdigest()


def concatenate_bytearrays(bytearrays):
    """Concatenates list of bytearrays"""
    r = bytearray.fromhex(bytearrays[0])
    for h in bytearrays[1:]:
        r.extend(bytearray.fromhex(h))
    return r.hex()


def find_integer(s, nbits, modified=False):
    """Generates integer in [0,2^nbits - 1] from a seed s of 160-bit length
    modified = True corresponds to find_integer2 as defined by brainpool"""
    v = floor((nbits - 1) / 160)
    w = nbits - 160 * v
    if modified:
        w -= 1
    h = sha1(s)
    z = ZZ(s, 16)
    bytearrays = [rightmost_bits(h, w)]
    for i in range(1, v + 1):
        z_i = (z + i) % (2 ** 160)
        s_i = int_to_hex_string(z_i)
        bytearrays.append(sha1(s_i))
    h = concatenate_bytearrays(bytearrays)
    return ZZ(h, 16)


def check_for_prime(n):
    """Checks whether n is suitable as a base field prime"""
    if n % 4 != 3:
        return False
    return n.is_prime()


def gen_prime(s, nbits):
    """Generates a nbits prime out of 160bit seed s"""
    while True:
        p = find_integer(s, nbits)
        while not check_for_prime(p):
            p += 1
        if 2 ** (nbits - 1) <= p <= 2 ** nbits - 1:
            return p
        s = update_seed(s)


def find_a(field, s, nbits):
    """Out of 160bit seed s, finds coefficient a for y^2=x^3+ax+b over F_p where p has nbits"""
    z = PolynomialRing(field, 'z').gen()
    while True:
        a = find_integer(s, nbits, modified=True)
        if (a * z ** 4 + 3).roots():
            return a, s
        s = update_seed(s)


def find_b(field, s, nbits):
    """Out of 160bit seed s, finds coefficient b for y^2=x^3+ax+b over F_p where p has nbits"""
    while True:
        b = find_integer(s, nbits, modified=True)
        if not field(b).is_square():
            return b, s
        s = update_seed(s)


def check_discriminant(a, b, p):
    """Checks whether discriminant of y^2=x^3+ax+b over F_p is nonzero"""
    return (4 * a ** 3 + 27 * b ** 2) % p != 0


def embedding_degree_q(q, r):
    """returns embedding degree with respect to q"""
    return Integers(r)(q).multiplicative_order()


def class_number_check(curve, q, bound):
    """Tests whether the class number of curve is bounded by bound"""
    p = curve.base_field().order()
    t = p + 1 - q
    ndisc = t ** 2 - 4 * p
    disc = squarefree_part(-ndisc)
    if disc % 4 != 1:
        disc *= 4
    if disc % 4 == 0:
        neutral = BinaryQF([1, 0, -ndisc // 4])
    else:
        neutral = BinaryQF([1, 1, (1 - ndisc) // 4])
    class_lower_bound = 1

    def test_form_order(quad_form, order_bound, neutral_element):
        """Tests whether an order of quadratic form is smaller then bound"""
        tmp = quad_form
        for i in range(1, order_bound):
            if tmp.is_equivalent(neutral_element):
                return i
            tmp *= form
        return -1

    for a in xsrange(1, Integer(1 + ((-ndisc) // 3)).isqrt()):
        a4 = 4 * a
        s = ndisc + a * a4
        w = 1 + (s - 1).isqrt() if s > 0 else 0
        if w % 2 != ndisc % 2:
            w += 1
        for b in xsrange(w, a + 1, 2):
            t = b * b - ndisc
            if t % a4 == 0:
                c = t // a4
                if gcd([a, b, c]) == 1:
                    if 0 < b < a < c:
                        form = BinaryQF([a, -b, c])
                    else:
                        form = BinaryQF([a, b, c])
                    order = test_form_order(form, bound, neutral)
                    if order == -1:
                        return True
                    class_lower_bound = lcm(class_lower_bound, order)
                    if class_lower_bound > bound:
                        return True
    return False


def security(curve, q):
    """Checks security conditions for curve"""
    p = curve.base_field().order()

    # 1
    if q >= p:
        return False

    # 2
    if p + 1 - q == 1:
        return False

    # 3
    if not q.is_prime():
        return False

    # 4
    emb_deg = embedding_degree_q(p, q)
    if not (q - 1) / emb_deg < 100:
        return False

    # 5
    if CHECK_CLASS_NUMBER and not class_number_check(curve, q, 10 ** 7):
        return False

    return True


def find_generator(scalar, field, curve):
    """Finds generator of curve as scalar*P where P has smallest x-coordinate"""
    a, b = curve.a4(), curve.a6()
    x = None
    for x in field:
        if (x ** 3 + a * x + b).is_square():
            break
    y = (x ** 3 + a * x + b).sqrt()
    y *= (-1) ** (randint(0, 1))
    point = curve(x, y)
    return scalar * point


def gen_curve(p, s, nbits):
    """Generates Brainpool curve over F_p (number of bits of p is nbits) out of 160bit seed"""
    field = GF(p)
    curve, q = None, None
    while True:
        a, s = find_a(field, s, nbits)
        s = update_seed(s)
        b, s = find_b(field, s, nbits)
        if not check_discriminant(a, b, p):
            s = update_seed(s)
            continue
        curve = EllipticCurve(field, [a, b])
        q = curve.__pari__().ellsea(1)
        if q == 0:
            s = update_seed(s)
            continue
        q = Integer(q)
        if not security(curve, q):
            s = update_seed(s)
            continue
        break
    s = update_seed(s)
    k = find_integer(s, nbits, modified=True)
    return curve, find_generator(k, field, curve), q


def test_gen_curve():
    """Testing of gen_curve on standardized Brainpool curves"""
    with open("testing_parameters_brainpool.json", "r") as file:
        brainpools = json.load(file)
    for nbits, curve_dict in brainpools.items():
        nbits = Integer(nbits)
        p = gen_prime(curve_dict['prime_seed'], nbits)
        assert int_to_hex_string(p) == curve_dict['p']

        curve, gen, q = gen_curve(p, curve_dict['seed'], nbits)
        x, y = Integer(gen[0]), Integer(gen[1])
        a, b = Integer(curve.a4()), Integer(curve.a6())

        def pad_zeros(hex_string):
            return (nbits // 4 - len(hex_string)) * "0" + x

        assert int_to_hex_string(a) == pad_zeros(curve_dict['A'])
        assert int_to_hex_string(b) == pad_zeros(curve_dict['B'])
        assert int_to_hex_string(q) == pad_zeros(curve_dict['order'])
        assert int_to_hex_string(x) == pad_zeros(curve_dict['x'])

