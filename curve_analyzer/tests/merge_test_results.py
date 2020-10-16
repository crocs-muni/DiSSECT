#!/usr/bin/env sage

import argparse
import json
import os
import re
from collections import OrderedDict

from curve_analyzer.definitions import TEST_PATH
from curve_analyzer.utils.json_handler import load_from_json, save_into_json

def dict_update_rec(a,b):
    for key in b.keys():
        if not key in a.keys():
            a[key] = b[key]
            continue
        b_value = b[key]
        a_value = a[key]
        if isinstance(a_value,dict):
            dict_update_rec(a_value,b_value)
        else:
            a_value = b_value
        a[key] = a_value


parser = argparse.ArgumentParser(description='Test results merger')
parser.add_argument('-n', '--test_name', type=str, help='Name of the test')
args = parser.parse_args()
test_name = args.test_name
assert re.search(r'[ais][0-9][0-9]', test_name)



# initialize original results
results_file_name = os.path.join(TEST_PATH, test_name, test_name + '.json')
if os.path.isfile(results_file_name):
    total_results = load_from_json(results_file_name)
else:
    total_results = {}

# iterate through partial results and merge them together with the original ones, then delete them
for root, _, files in os.walk(os.path.join(TEST_PATH, test_name)):
    for file in files:
        if file.split('.')[-1] != 'json' or "part" not in file:
            continue
        fname = os.path.join(root, file)
        with open(fname, 'r') as f:
            partial_results = OrderedDict(json.load(f))
        partial_results_sorted = sorted(partial_results.items())
        dict_update_rec(total_results,partial_results_sorted)#total_results.update(partial_results_sorted)
        tmp_file_name = os.path.join(TEST_PATH, test_name, test_name + '.tmp')
        save_into_json(total_results, tmp_file_name, 'w+')
        os.remove(fname)

        # delete the old result file and rename the temp one
        try:
            os.remove(results_file_name)
        except OSError:
            pass
        os.rename(tmp_file_name, results_file_name)
