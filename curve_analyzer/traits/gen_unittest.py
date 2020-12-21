#!/usr/bin/env sage
import argparse
import json
import sys
from pathlib import Path

from curve_analyzer.definitions import TRAIT_PATH, TRAIT_MODULE_PATH, TRAIT_NAMES
from curve_analyzer.traits.example_curves import curves
from curve_analyzer.utils.json_handler import save_into_json, load_from_json


def load_params_local(local_params):
    if local_params:
        print("Input parameters: ")
    params = []
    for param_name in local_params:
        try:
            param_value = json.loads(input(param_name + ": "))
        except json.decoder.JSONDecodeError:
            print("Invalid format")
            return False
        params.append(param_value)
    return params


def create_structure_file(name):
    with open(Path(TRAIT_PATH, name, name + ".params"), "r") as f:
        params = json.loads(f.read())
    params_names = params["params_local_names"]
    params = load_params_local(params_names)

    module_name = TRAIT_MODULE_PATH + '.' + name + '.' + name
    __import__(module_name)
    curve_function = getattr(sys.modules[module_name], name + "_curve_function")

    result = {}
    for curve in curves:
        print("Curve " + curve.name + ": ")
        result[curve.name] = {}
        computed_result = curve_function(curve, *params)
        for key in computed_result.keys():
            try:
                key_result = json.loads(input("Result for " + key + ": "))
            except json.decoder.JSONDecodeError:
                print("Invalid format")
                return False
            if computed_result[key] != key_result and str(computed_result[key]) != key_result:
                print("Wrong result, should be: " + str(computed_result[key]))
                return False
        result[curve.name][str(dict(zip(params_names, params)))] = computed_result
    json_file = Path(TRAIT_PATH, name, name + '_structure.json')
    save_into_json(result, json_file, mode='w')
    return True


def create_unittest(name):
    results = load_from_json(Path(TRAIT_PATH, name, name + "_structure.json"))
    if Path(TRAIT_PATH, "unit_tests", "trait_" + name + ".py").is_file():
        answer = input("Unittest for " + name + " already exists, overwrite? [Y/n]")
        if answer in "[n,N]":
            return
    f = open(Path(TRAIT_PATH, "unit_tests", "trait_" + name + ".py"), "w")

    f.write("import unittest, ast\n")
    f.write("from curve_analyzer.traits." + name + "." + name + " import " + name + "_curve_function\n")
    f.write("from curve_analyzer.traits.example_curves import curves, curve_names\n")
    f.write("results=" + str(results) + "\n")
    f.write("\nclass Test" + name[0].upper() + name[1:] + "(unittest.TestCase):\n \n")
    for curve in results.keys():
        f.write("    def test_auto_generated_" + str(curve) + "(self):\n")
        f.write("        '''This test has been auto-generated by gen_unittest'''\n")
        f.write("        params = ast.literal_eval(list(results[\"" + str(curve) + "\"].keys())[0]).values()\n")
        f.write("        computed_result = " + name + "_curve_function(curve_names[\"" + str(curve) + "\"],*params)\n")
        f.write("        self.assertEqual(computed_result,list(results[\"" + str(curve) + "\"].values())[0])\n\n")
    f.write("\nif __name__ == '__main__':\n")
    f.write("   unittest.main()\n")
    f.write("   print(\"Everything passed\")\n")

    f.close()


tests_to_skip = ['a08']


def main():
    parser = argparse.ArgumentParser(
        description='Create unit traits or structure files or both(default).')
    parser.add_argument("-u", action='store_true', help='only unittest flag (default: False)')
    parser.add_argument('-s', action='store_true', help='only structure file flag (default: False)')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-n', '--trait_name', metavar='trait_name', type=str, action='store',
                               help='List names of the traits seperated by comma or all; available traits: ' + ", ".join(
                                   TRAIT_NAMES), required=True)

    args = parser.parse_args()
    if args.trait_name == "all":
        trait_name = TRAIT_NAMES
    else:
        trait_name = [n.strip() for n in args.trait_name.split(",")]
    trait_name = list(set(trait_name) - set(traits_to_skip))
    for name in trait_name:
        if args.u:
            create_unittest(name)
            continue
        if args.s:
            create_structure_file(name)
            continue
        if create_structure_file(name):
            create_unittest(name)


if __name__ == '__main__':
    main()
