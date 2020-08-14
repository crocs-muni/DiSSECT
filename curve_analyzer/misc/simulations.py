from sage.all import *
from curve_analyzer.utils.json_handler import *
import hashlib

#hex string to binary string
def sha1_bin(x):
    return format(ZZ(hashlib.sha1(bytes.fromhex(x)).hexdigest(), 16), '0160b')

def sha1_hex(x):
    return format(ZZ(sha1(x), 2), '0160x')

def int_to_hex_string(x):
    f = '0' + str(ceil(x.nbits()/8)*2) + 'X'
    return format(ZZ(x, 16), f)

def increment_seed(seed, i = 1):
    f = '0' + str(ceil(x.nbits()/8)*2) + 'X'
    return format(ZZ(x, 16), f)

def increment_seed(seed, i = 1):
    '''accepts a hex string as input (not starting with 0x)'''
    g = ZZ(seed, 16).nbits()
    f = '0' + str(len(seed)) + 'X'
    return format(ZZ(Mod(ZZ(seed, 16) + i, 2^g)), f)

#http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.202.2977&rep=rep1&type=pdf, page 42
def generate_r(seed, p):
    t = p.nbits()
#     t = ceil(log(p,2))
#     originally floor
    s = floor((t-1)/160)
    h = t - 160 * s
#     print("t:",t, "s:", s, "h:", h)
    H = sha1_bin(seed)
    c0  = H[-h:]
    c0_modified = list(c0)
    c0_modified[0] = '0'
    W = [0] * (s + 1)
    W[0] =  ''.join(c0_modified)
    for i in [1..s]:
        input_i = increment_seed(seed, i)
        W[i] = sha1_bin(input_i)
    W_joint = ''.join(W)
    assert(len(W_joint) == t)
    r = 0
    for i in [1..t]:
        r += ZZ(W_joint[i-1]) * 2^(t-i)
    assert(r == ZZ(W_joint, 2))
    F = GF(p)
    return F(r)

def expected_r(p, a, b):
    F = GF(p)
    return F(a^3/b^2)

def verify_r(p, r, a, b):
    F = GF(p)
    return F(r) == expected_r(p, a, b)

def get_b_from_r(r, p, a = -3):
    F = GF(p)
    if F(a^3/r).is_square():
        return ZZ(F(a^3/r).sqrt())
    else:
        return None

def has_root(pol, p):
    R.<x> = PolynomialRing(GF(p))
    S = R.quotient(pol, 'a')
    f1 = S(x)
    res = S(1)
    for bit in p.bits():
        if bit == 1:
            res *= f1
        f1 = S(f1^2)
    return gcd(pol, res.lift() - x).degree() > 0

def has_points_of_low_order(E, l_max = 4, poly_method = 'division'):
    assert poly_method in ['division', 'modular']
    p = E.base_field().order()
    R = PolynomialRing(GF(p), 'x')
    x = R.gen()
    
    if poly_method == 'modular': #non-deterministic method
        mdb = ClassicalModularPolynomialDatabase() 
        for l in prime_range(l_max):
            j = E.j_invariant()
            pol = R(mdb[l](j,x))
            if has_root(pol, p):
                return True
            else:
                continue
    
    if poly_method == 'division': #deterministic method, useful for 256 bits with l_max = 4
        weier = x^3 + x * E.ainvs()[-2] + E.ainvs()[-1]
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

def millerrabinliar(n,a):
    r = 0
    m = n-1
    while m % 2 == 0:
        r += 1
        m = m/2
    if Mod(a,n)^m == Mod(1,n):
        return True
    for i in range(r):
        if Mod(a,n)^(m*2^i) == Mod(-1,n):
            return True
    return False

def millerrabin(n):
    for a in prime_range(200):
        if not millerrabinliar(n, a):
            return False
    return True

# A2.2 in http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.202.2977&rep=rep1&type=pdf
def verify_near_primality(u, r_min, l_max = 255, MR = True):
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

def verify_security(E, r_min_bits = 160, B = 20, MR = True, verbose = False):
    if verbose:
        print("Computing order")
    q = E.base_field().order()
    r_min = max(2^r_min_bits, 4 * sqrt(q))
    o = E.order()
    if verbose:
        print("Checking near-primality of", o)
    alright, h, n = verify_near_primality(o, r_min, MR = MR)
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

def generate_x962_curves(count, p, curve_seed, seed_offset = 0, increment_step = 1, fixed_a = True, verify = True, r_min_bits = 160, save_to_json = True, jsonfile = "curves_json/x962-sim/curves.json", logfile = "curves_json/x962-sim/curves.log", MR = True, overwrite = False, verbosity_freq = 1000, l_max = 20):
    assert fixed_a
    a = -3
    
    if os.path.exists(jsonfile) and not overwrite:
        print("The result file already exists! Aborting...")
        return
    
    def feedback(text, frmt = '{:s}', outfile = logfile):
        print(text, end='')
        with open(outfile, 'a') as f:
            f.write(frmt.format(text))
    with open(logfile, 'w'):
        pass
    
    seed = increment_seed(curve_seed, seed_offset)
    bits = p.nbits()
    feedback("Generating " + str(bits) + "-bit curves from the initial seed " + str(seed) + " offset by " + str(seed_offset) + "...\n")
    sim_curves = {}
    sim_curves["name"] = "x962_sim_" + str(bits)
    sim_curves["desc"] = "simulated curves generated according to the X9.62 standard using the initial seed " + str(seed) + " (the standard seed offset by " + str(seed_offset) + ")"
    sim_curves["curves_tried"] = count
    sim_curves["curves"] = []
    
    rel_seed = 0
    start_time = time.time()
    total_time = 0
    for i in [1..count]:
        rel_seed = increment_step * i
        if i%verbosity_freq == 0:
            end_time = time.time()
            diff_time = end_time - start_time
            total_time += diff_time
            feedback(str(i) + " out of " + str(count) + " curves tried, currently at seed " + str(int_to_hex_string(rel_seed)) + ", time elapsed: " + str(diff_time) + "\n")
            start_time = time.time()
        seed_i = increment_seed(seed, increment_step * i)
        r = generate_r(seed_i, p)
        b = get_b_from_r(r, p)
        if b == None or 4 * a ** 3 + 27 * b ** 2 == 0:
            continue
        E = EllipticCurve(GF(p), [a,b])
        
#         t1 = time.time()
        has_points = has_points_of_low_order(E, l_max, poly_method = 'division')
#         t2 = time.time()
#         print(t2-t1)
        if has_points:
            continue
        
        alright, h, n = verify_security(E, r_min_bits, MR = MR)
        if alright:
            assert h*n == E.order() #might not be needed
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
    feedback(90 * '.' + "\n" + "Finished, total time elapsed: " + str(total_time))
    sim_curves["curves_total"] = len(sim_curves["curves"])
    if save_to_json:
        save_into_json(sim_curves, jsonfile)
    return sim_curves

def generate_x962_standard_like_curves(bitlen, count, offset = 0, save_to_json = True, overwrite = False, verbosity_freq = 1000, l_max = 20):
    #bitlens, primes and corresponding seeds, case a=-3 (curves r1, prime fields only)
    # https://www.secg.org/sec2-v2.pdf
    x962_params = []
    x962_params.append((112, 0xDB7C2ABF62E35E668076BEAD208B, '00F50B028E4D696E676875615175290472783FB1'))
    x962_params.append((128, 0xFFFFFFFDFFFFFFFFFFFFFFFFFFFFFFFF, '000E0D4D696E6768756151750CC03A4473D03679'))
    x962_params.append((160, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7FFFFFFF, '1053CDE42C14D696E67687561517533BF3F83345'))
    x962_params.append((192, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFF, '3045AE6FC8422F64ED579528D38120EAE12196D5'))
    x962_params.append((224, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF000000000000000000000001, 'BD71344799D5C7FCDC45B59FA3B9AB8F6A948BC5'))
    x962_params.append((256, 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF, 'C49D360886E704936A6678E1139D26B7819F7E90'))
    x962_params.append((384, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFF, 'A335926AA319A27A1D00896A6773A4827ACDAC73'))
    x962_params.append((521, 0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, 'D09E8800291CB85396CC6717393284AAA0DA64BA'))
    
    for bits, p, seed in x962_params:
        assert p.nbits() == bits
        assert len(seed) == 40
        if bits == bitlen:
            jsonfile = 'curves_json/x962-sim/curves' + str(bits) + '.json'
            logfile = 'curves_json/x962-sim/curves' + str(bits) + '.log'
            return generate_x962_curves(count, p, seed, offset, -1, r_min_bits = bits-10, save_to_json = save_to_json, jsonfile = jsonfile, logfile = logfile, overwrite = overwrite, verbosity_freq = verbosity_freq, l_max = l_max)