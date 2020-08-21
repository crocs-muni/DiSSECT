"""
Sage script containing the functions for the experiment.
Has CLI so we can start experiments directly from the CLI.

User can specify job to compute either via CLI or as
a JSON config file (not implemented here).

After experiment is finished, the script writes results to the output file.
"""

import json
import argparse
from sage.all import ZZ
from curve_analyzer.utils.json_handler import IntegerEncoder
from curve_analyzer.utils.simulations_x962 import generate_x962_curves

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sage experiment runner')

    parser.add_argument('-c', '--count', action='store', help='')
    parser.add_argument('-p', '--prime', action='store', help='')
    parser.add_argument('-s', '--seed', action='store', help='')
    parser.add_argument('-f', '--outfile', action='store', help='')
    args = parser.parse_args()
    print(args)

    # Do the computation
    count = ZZ(args.count)
    p = ZZ(args.prime)
    seed = args.seed
    r = generate_x962_curves(count, p, seed)

    # Save results to the output file
    with open(args.outfile, 'w+') as fh:
        json.dump(r, fh, cls = IntegerEncoder)
