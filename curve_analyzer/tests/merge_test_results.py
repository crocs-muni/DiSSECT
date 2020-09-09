#!/usr/bin/env sage

import argparse
import json
import os
import re
from collections import OrderedDict

from curve_analyzer.definitions import TEST_PATH
from curve_analyzer.tests.test_interface import get_timestamp
from curve_analyzer.utils.json_handler import load_from_json, save_into_json

parser = argparse.ArgumentParser(description='Test results merger')
parser.add_argument('-n', '--test_name', type=str, help='Name of the test')
args = parser.parse_args()
test_name = args.test_name
assert re.search(r'[ais][0-9][0-9]', test_name)

# iterate through partial results and merge them together
partial_results_filenames = []
merged = OrderedDict({})
for root, _, files in os.walk(os.path.join(TEST_PATH, test_name)):
    for file in files:
        if file.split('.')[-1] != 'json' or "part" not in file:
            continue
        fname = os.path.join(root, file)
        partial_results_filenames.append(fname)
        with open(fname, 'r') as f:
            results = json.load(f)
            merged.update(results)

# merge all the results with the original ones, sort and save them as a temp file
results_file_name = os.path.join(TEST_PATH, test_name, test_name + '.json')
if os.path.isfile(results_file_name):
    total_results = load_from_json(results_file_name)
else:
    total_results = {}

total_results.update(sorted(merged.items()))
total_results_ordered = OrderedDict(sorted(total_results.items()))
merged_file_name = os.path.join(TEST_PATH, test_name, test_name + '_' + get_timestamp() + '.tmp')
save_into_json(total_results_ordered, merged_file_name, 'w+')

# delete the original results and the partial results and rename the temp file
for file in partial_results_filenames:
    os.remove(file)
try:
    os.remove(results_file_name)
except OSError:
    pass
os.rename(merged_file_name, results_file_name)
