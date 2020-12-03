#!/usr/bin/env sage

from pathlib import Path
from curve_analyzer.definitions import TEST_PATH, TEST_NAMES
from curve_analyzer.utils.json_handler import load_from_json, save_into_json


def dict_update_rec(a, b):
    for key in b.keys():
        if key not in a.keys():
            a[key] = b[key]
            continue
        b_value = b[key]
        a_value = a[key]
        if isinstance(a_value, dict):
            dict_update_rec(a_value, b_value)
        else:
            a_value = b_value
        a[key] = a_value

def merge_results(test_name):

    # initialize original results
    results_file_name = Path(TEST_PATH, test_name, test_name + '.json')
    if results_file_name.is_file():
        total_results = load_from_json(results_file_name)
    else:
        total_results = {}

    # iterate through partial results in the same folder and merge them together with the original ones, then delete them
    files = [item for item in Path(TEST_PATH, test_name).iterdir() if item.is_file()]
    for file in files:
        if file.suffix != '.json' or "part" not in file.name:
            continue
        partial_results = load_from_json(file)

        dict_update_rec(total_results, partial_results)
        tmp_file_name = Path(TEST_PATH, test_name, test_name + '.tmp')
        save_into_json(total_results, tmp_file_name, 'w+')
        file.unlink()

        # delete the old result file and rename the temp one
        try:
            results_file_name.unlink()
        except FileNotFoundError:
            pass

        tmp_file_name.rename(results_file_name)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Test results merger')
    parser.add_argument('-n', '--test_name', type=str, help='Name of the test')
    args = parser.parse_args()
    test_name = args.test_name
    if test_name not in TEST_NAMES:
        print("please enter a valid test identifier, e.g., a02")
        exit()

    merge_results(test_name)
