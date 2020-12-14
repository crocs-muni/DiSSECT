#!/usr/bin/env sage
import itertools
import json
import optparse
import sys
from pathlib import Path

from sage.misc.sage_eval import sage_eval

from curve_analyzer.definitions import TEST_PATH, TEST_MODULE_PATH, TEST_NAMES
from curve_analyzer.tests.example_curves import curves
from curve_analyzer.utils.json_handler import save_into_json, load_from_json

tests_to_skip = ['a08']


def compute_results(test_name):
    module_name = TEST_MODULE_PATH + '.' + test_name + '.' + test_name
    __import__(module_name)
    curve_function = getattr(sys.modules[module_name], test_name + "_curve_function")
    params_file = Path(TEST_PATH, test_name, test_name + '.params')
    results = {}
    for curve in curves:
        results[curve.name] = {}
    with open(params_file, 'r') as f:
        params = json.load(f)
    for key in params["params_global"].keys():
        params["params_global"][key] = sage_eval(params["params_global"][key])
    params_global = params["params_global"]
    params_local_names = params["params_local_names"]
    params_local_values = list(itertools.product(*params_global.values()))[0]
    params_local = dict(zip(params_local_names, params_local_values))
    for curve in curves:
        results[curve.name][str(params_local)] = curve_function(curve, *params_local_values)

    # Generate/update structure file
    structure_file = Path(TEST_PATH, test_name, test_name + '_structure' + '.json')
    if structure_file.is_file():
        old_results = load_from_json(structure_file)
        if old_results != results:
            save_into_json(results, structure_file, mode='w')
            print("Structure file updated for ", test_name)
    else:
        save_into_json(results, structure_file, mode='w')
        print("Structure file created for ", test_name)


def main(imported=False):
    if imported:
        for filename in TEST_NAMES:
            if filename in tests_to_skip:
                continue
            compute_results(filename)
        return
    parser = optparse.OptionParser()
    parser.add_option('-t', '--test',
                      action="store", dest="test",
                      help="list of names for structure generation separated by comma or \'all\'", default="all")
    options, args = parser.parse_args()
    if options.test == "all":
        for filename in TEST_NAMES:
            if filename in tests_to_skip:
                continue
            compute_results(filename)
    else:
        tests = options.test.split(",")
        for name in tests:
            compute_results(name)


if __name__ == '__main__':
   main()
