"""
Sage script containing the functions for the experiment.
Has CLI so we can start experiments directly from the CLI.

User can specify job to compute either via CLI or as
a JSON config file (not implemented here).

After experiment is finished, the script writes results to the output file.
"""

import json
import argparse


def benchmark1(inp):
    r = factor(inp)
    return r


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sage experiment runner')
    parser.add_argument('-i', '--input', type=int, default=941239804723908471390247123492147901647126341, help='Input')

    parser.add_argument('-c', '--count', action='store', help='')
    parser.add_argument('-p', '--prime', action='store', help='')
    parser.add_argument('-s', '--seed', action='store', help='')
    parser.add_argument('-f', '--outfile', action='store', help='')
    args = parser.parse_args()

    # generate_x962_curves(args.count, args.prime, args.seed, jsonfile= args.outfile)

    # Do the computation
    r = benchmark1(args.input)

    # Save results to the output file
    with open(args.outfile, 'w+') as fh:
        json.dump(str(list(r)), fh)
