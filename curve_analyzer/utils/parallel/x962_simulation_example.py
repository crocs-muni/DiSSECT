"""
Sage script containing the functions for the experiment.
Has CLI so we can start experiments directly from the CLI.

User can specify job to compute either via CLI or as
a JSON config file (not implemented here).

After experiment is finished, the script writes results to the output file.
"""

import json
import argparse
from simulations import generate_x962_curves
from sage.all import ZZ
from sage.all import *
import sage
# from ..curve_analyzer.curve_analyzer.misc.simulations import generate_x962_curves

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sage experiment runner')
    # parser.add_argument('-i', '--input', type=int, default=941239804723908471390247123492147901647126341, help='Input')

    parser.add_argument('-c', '--count', action='store', help='')
    parser.add_argument('-p', '--prime', action='store', help='')
    parser.add_argument('-s', '--seed', action='store', help='')
    parser.add_argument('-f', '--outfile', action='store', help='')
    args = parser.parse_args()

    # generate_x962_curves(args.count, args.prime, args.seed, jsonfile= args.outfile)

    # Do the computation
    count = ZZ(args.count)
    p = ZZ(args.prime)
    seed = args.seed

    # print(args)
    r = generate_x962_curves(count, p, seed)

    class IntegerEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, sage.rings.integer.Integer):
                return int(obj)

            if isinstance(obj, sage.rings.polynomial.polynomial_modn_dense_ntl.Polynomial_dense_mod_p):
                return str(obj)

            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, obj)

    # Save results to the output file
    with open(args.outfile, 'w+') as fh:
        json.dump(r, fh, cls = IntegerEncoder)
