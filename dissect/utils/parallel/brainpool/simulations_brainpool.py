"""This is an implementation of the Brainpool standard suitable for large-scale simulations
    For more readable implementation, see the brainpool.py
"""

from sage.all import ZZ, PolynomialRing, GF, EllipticCurve, Integer
import json

from dissect.utils.parallel.brainpool.brainpool import find_integer, update_seed, check_discriminant, security, \
    find_generator, int_to_hex_string


def generate_brainpool_curves(count, p, seed):
    """Custom function for generating large number of Brainpool curves"""
    bits = p.nbits()
    sim_curves = {
        "name": "brainpool_sim_" + str(bits),
        "desc": "simulated curves generated according to the Brainpool standard",
        "initial_seed": seed,
        "seeds_tried": count,
        "curves": [],
        "seeds_successful": 0,
    }

    with open("brainpool/parameters_brainpool.json", "r") as f:
        params = json.load(f)
        original_seed = params[str(bits)][1]

    field = GF(p)
    z = PolynomialRing(field, 'z').gen()
    a = None
    for i in range(1, count + 1):
        if a is None:
            a = find_integer(seed, bits, modified=True)
            if not (a * z ** 4 + 3).roots():
                a = None
                seed = update_seed(seed)
                continue
            seed = update_seed(seed)
        b = find_integer(seed, bits, modified=True)
        if field(b).is_square():
            seed = update_seed(seed)
            continue
        if not check_discriminant(a, b, p):
            seed = update_seed(seed)
            a = None
            continue
        curve = EllipticCurve(field, [a, b])
        q = curve.__pari__().ellsea(1)
        if q == 0:
            seed = update_seed(seed)
            a = None
            continue
        q = Integer(q)
        if not security(curve, q):
            seed = update_seed(seed)
            a = None
            continue
        k = find_integer(update_seed(seed), bits, modified=True)
        gen = find_generator(k, field, curve)
        x, y = Integer(gen[0]), Integer(gen[1])

        seed_diff = ZZ("0X" + seed) - ZZ("0X" + original_seed)
        sim_curve = {
            "name": "brainpool_sim_" + str(bits) + "_seed_diff_" + str(seed_diff),
            "category": sim_curves["name"],
            "desc": "",
            "field": {
                "type": "Prime",
                "p": int_to_hex_string(p, prefix=True, lower_case=True),
                "bits": bits,
            },
            "form": "Weierstrass",
            "params": {"a": {"raw": int_to_hex_string(a, prefix=True, lower_case=True)},
                       "b": {"raw": int_to_hex_string(b, prefix=True, lower_case=True)}},
            "generator": {"x": {"raw": int_to_hex_string(x, prefix=True, lower_case=True)},
                          "y": {"raw": int_to_hex_string(y, prefix=True, lower_case=True)}},
            "order": q,
            "cofactor": 1,
            "characteristics": None,
            "seed": seed,
            "seed_diff": seed_diff,
        }
        sim_curves["curves"].append(sim_curve)
        sim_curves["seeds_successful"] += 1
        seed = update_seed(seed)

    return sim_curves


def test_generate_brainpool_curves():
    with open("testing_parameters_brainpool.json", "r") as f:
        params = json.load(f)
        for bits,curve in params.items():
            seed = curve["correct_seed"]
            p = Integer(int(curve["p"],16))
            curves = generate_brainpool_curves(5,Integer(p),seed)["curves"]
            print(bits)
            assert len(curves)==1
