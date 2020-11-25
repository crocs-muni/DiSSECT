#!/usr/bin/env sage
import itertools,optparse
from curve_analyzer.utils.json_handler import *
from curve_analyzer.definitions import TEST_PATH, TEST_MODULE_PATH, TEST_prefixes
from curve_analyzer.tests.testing_curves import curves

tests_to_skip = ['a08']

def compute_results(test_name):
    module_name = TEST_MODULE_PATH+'.'+test_name + '.' + test_name
    __import__(module_name)
    curve_function = getattr(sys.modules[module_name], test_name+"_curve_function")
    main_json_file = os.path.join(TEST_PATH, test_name, test_name +'_structure'+ '.json')
    params_file = os.path.join(TEST_PATH, test_name, test_name + '.params')
    results= {}
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
    save_into_json(results,main_json_file,mode = 'w')



def main():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--test',
                      action="store", dest="test",
                      help="list of names for structure generation seperated by comma or \'all\'", default="all")
    options, args = parser.parse_args()
    if options.test== "all":
        directory = TEST_PATH
        for filename in os.listdir(directory):
            if filename in tests_to_skip:
                continue
            if not filename[0] in TEST_prefixes:
                continue
            try:
                int(filename[1:],10)
            except:
                continue
            compute_results(filename)
    else:
        tests = options.test.split(",")
        for name in tests:
            compute_results(name)

main()





