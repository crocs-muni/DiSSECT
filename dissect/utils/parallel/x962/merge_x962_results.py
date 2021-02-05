#!/usr/bin/env sage

import json
import os

from dissect.definitions import PARALLEL_RESULTS_PATH, X962_PATH
from dissect.utils.json_handler import IntegerEncoder
from dissect.utils.parallel.x962.simulations_x962 import increment_seed

X962_RESULTS = os.path.join(PARALLEL_RESULTS_PATH, 'x962')
VERBOSE = False

# get the names of immediate subdirs, which should be the respective bitsizes
bitsizes = [f.name for f in os.scandir(X962_RESULTS) if f.is_dir()]

for bitsize in bitsizes:
    results_path = os.path.join(X962_RESULTS, bitsize)
    # skip empty dirs
    if len(os.listdir(results_path)) == 0:
        continue

    with open(os.path.join(X962_PATH, 'parameters_x962.json'), 'r') as f:
        params = json.load(f)
        original_seed = params[bitsize][1]
    merged = None

    for root, _, files in os.walk(results_path):
        # iterate through result files, starting with largest seeds
        for file in sorted(files, key=lambda x: int((x.split('.')[-2]).split('_')[-1], 16), reverse=True):
            fname = os.path.join(root, file)
            with open(fname, 'r') as f:
                results = json.load(f)
                if VERBOSE:
                    print('Merging ', fname, '...')

                if merged is None:
                    merged = results
                    expected_initial_seed = original_seed
                else:
                    expected_initial_seed = increment_seed(original_seed, -merged["seeds_tried"])
                    merged["curves"] += results["curves"]
                    merged["seeds_tried"] += results["seeds_tried"]
                    merged["seeds_successful"] += results["seeds_successful"]
                # check seed continuity
                try:
                    assert (expected_initial_seed == results["initial_seed"])
                except AssertionError:
                    raise ValueError('The expected initial seed is ', expected_initial_seed, ' but the current one is ',
                                     results["initial_seed"])

    # save the merged results into a temp file, then delete all others, then rename it
    merged_name = os.path.join(results_path,
                               str(merged["seeds_tried"]) + '_' + str(bitsize) + '_' + original_seed + '.json')
    merged_name_tmp = merged_name + '.tmp'
    with open(merged_name_tmp, 'w+') as fh:
        json.dump(merged, fh, cls=IntegerEncoder)

    for root, _, files in os.walk(results_path):
        for file in sorted(files, reverse=True):
            fname = os.path.join(root, file)
            if os.path.splitext(fname)[1] != '.tmp':
                os.remove(fname)
    os.rename(merged_name_tmp, merged_name)
