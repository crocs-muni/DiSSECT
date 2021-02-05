#!/usr/bin/env sage

import argparse
from pathlib import Path

from dissect.definitions import TRAIT_PATH, TRAIT_NAMES
from dissect.utils.json_handler import load_from_json, save_into_json


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


def merge_results(trait_name, verbose=False):
    """Merge all JSONS with partial results of the given trait together with current results. Assumes that the partial
    results will fit into memory. """

    # iterate through partial results in the same folder and interatively merge them together
    new_results = {}
    files = sorted([item for item in Path(TRAIT_PATH, trait_name).iterdir() if
                    item.is_file() and item.suffix == '.json' and "part" in item.name])
    for file in files:
        partial_results = load_from_json(file)
        dict_update_rec(new_results, partial_results)
        if verbose:
            print("Results from " + file.name + " merged")

    # merge the new results with the old ones, if they exist
    total_results_name = Path(TRAIT_PATH, trait_name, trait_name + '.json')
    if total_results_name.is_file():
        if verbose:
            print("Merging with the old results...")
        total_results = load_from_json(total_results_name)
        dict_update_rec(new_results, total_results)
        tmp_file_name = Path(TRAIT_PATH, trait_name, trait_name + '.tmp')
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


def main():
    parser = argparse.ArgumentParser(description='Trait results merger')
    parser.add_argument('-n', '--trait_name', type=str, help='Name of the trait')
    parser.add_argument('-v', '--verbosity', action='store_true', help='verbosity flag (default: False)')
    args = parser.parse_args()
    if args.trait_name not in TRAIT_NAMES:
        print("please enter a valid trait identifier, e.g., a02")
        exit()

    merge_results(args.trait_name, verbose=args.verbosity)

if __name__ == '__main__':
    main()
