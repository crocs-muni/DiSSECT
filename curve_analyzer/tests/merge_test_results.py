#!/usr/bin/env sage

from pathlib import Path

from curve_analyzer.definitions import TEST_PATH, TEST_NAMES
from curve_analyzer.utils.json_handler import load_from_json, save_into_json


def dict_update_rec(a, b):
    """Recursively update the first dictionary using keys and values in the second."""
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


def merge_results(test_name, verbose=False):
    """Merge all JSONS with partial results of the given test together with current results. Assumes that the partial
    results will fit into memory. """

    # iterate through partial results in the same folder and interatively merge them together
    new_results = {}
    files = sorted([item for item in Path(TEST_PATH, test_name).iterdir() if
                    item.is_file() and item.suffix == '.json' and "part" in item.name])
    for file in files:
        partial_results = load_from_json(file)
        dict_update_rec(new_results, partial_results)
        if verbose:
            print("Results from " + file.name + " merged")

    # merge the new results with the old ones, if they exist
    total_results_name = Path(TEST_PATH, test_name, test_name + '.json')
    if total_results_name.is_file():
        if verbose:
            print("Merging with the old results...")
        total_results = load_from_json(total_results_name)
        dict_update_rec(new_results, total_results)
        tmp_file_name = Path(TEST_PATH, test_name, test_name + '.tmp')
        if verbose:
            print("Saving into JSON...")
        save_into_json(new_results, tmp_file_name, 'w+')
        total_results_name.unlink()
        tmp_file_name.rename(total_results_name)
    else:
        if verbose:
            print("Saving into JSON...")
        save_into_json(new_results, total_results_name, 'w+')

    # delete the partial results
    if verbose:
        print("Deleting old files...")
    for file in files:
        file.unlink()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Test results merger')
    parser.add_argument('-n', '--test_name', type=str, help='Name of the test')
    parser.add_argument('-v', '--verbosity', action='store_true', help='verbosity flag (default: False)')
    args = parser.parse_args()
    if args.test_name not in TEST_NAMES:
        print("please enter a valid test identifier, e.g., a02")
        exit()

    merge_results(args.test_name, verbose=args.verbosity)
