"""This is an implementation of the SEC standard suitable for large-scale simulations
    For more readable implementation, see the secg.py
"""
import json
from sage.all import EllipticCurve, GF, ZZ, Integer

from secg import increment_seed, get_b_from_r, generate_r, verify_security, int_to_hex_string, gen_point


def generate_secg_curves(count, p, seed, b_sign=False):
    """Custom function for generating large number of SEC curves"""
    bits = p.nbits()
    sim_curves = {
        "name": "secg_sim_" + str(bits),
        "desc": "simulated curves generated according to the SEC2 standard",
        "initial_seed": seed,
        "seeds_tried": count,
        "curves": [],
        "seeds_successful": 0,
    }

    with open("parameters_secg.json", "r") as f:
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

        secure, h, n = verify_security(E)
        if not secure:
            if not b_sign or p % 4 == 1:
                continue
            E = EllipticCurve(GF(p), [a, -b])
            secure, h, n = verify_security(E)
            if not secure:
                continue

        seed_diff = ZZ("0X" + original_seed) - ZZ("0X" + current_seed)
        sim_curve = {
            "name": "secg_sim_" + str(bits) + "_seed_diff_" + str(seed_diff),
            "category": sim_curves["name"],
            "desc": "",
            "field": {
                "type": "Prime",
                "p": int_to_hex_string(p),
                "bits": bits,
            },
            "form": "Weierstrass",
            "params": {"a": {"raw": int_to_hex_string(p - 3)}, "b": {"raw": int_to_hex_string(b)}},
            "generator": {"x": {"raw": ""}, "y": {"raw": ""}},
            "order": n,
            "cofactor": h,
            "characteristics": None,
            "seed": current_seed,
            "seed_diff": seed_diff,
        }
        sim_curves["curves"].append(sim_curve)
        sim_curves["seeds_successful"] += 1

    return sim_curves



def test_generate_secg_curves():
    """Testing of generate_secg_curves on standardized SEC curves"""
    with open("testing_parameters_secg.json", "r") as file:
        secg = json.load(file)
    for nbits, curve_dict in secg.items():
        nbits = Integer(nbits[4:-2])
        print(nbits)
        res = generate_secg_curves(1,ZZ(curve_dict['p'], 16), increment_seed(curve_dict['seed']), b_sign=True)['curves']
        assert len(res)==1
        curve = res[0]
        assert curve['params']['a']['raw'] == curve_dict['A']
        B = ZZ(curve['params']['b']['raw'],16)
        p = ZZ(curve['field']['p'],16)
        assert int_to_hex_string(B) == curve_dict['B'] or int_to_hex_string(p - B) == curve_dict['B']
        assert curve['field']['p'] == curve_dict['p']



