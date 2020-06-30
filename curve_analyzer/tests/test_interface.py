from sage.all_cmdline import *   # import sage library
from curve_analyzer.utils.curve_handler import *
from curve_analyzer.utils.json_handler import *
from curve_analyzer.definitions import TEST_PATH
from prettytable import PrettyTable  # http://zetcode.com/python/prettytable/
from collections import OrderedDict
import itertools
import time
import os
import ast

def feedback(text, outfile, frmt = '{:s}', newlines = 0):
    print(frmt.format(text), end = newlines * "\n")
    with open(outfile, 'a') as f:
        f.write(frmt.format(text))
        f.write(newlines * "\n")

def init_test(test_name):
    path_json = TEST_PATH + '/' + test_name + '/' + test_name + '.json'
    path_tmp = TEST_PATH + '/' + test_name + '/' + 'tmp.json'
    path_log = os.path.splitext(path_json)[0 ] + ".log"
    path_txt = os.path.splitext(path_json)[0 ] + ".txt"
    return path_json, path_tmp, path_log, path_txt

def handle_files(test_name):
    # assert the folder exists
    jsonfile, tmpfile, logfile, _ = init_test(test_name)
    if not os.path.exists(jsonfile):
        save_into_json({}, jsonfile, 'w')
    assert os.path.exists(jsonfile)
    with open(logfile, 'w'):
        pass
    return jsonfile, tmpfile, logfile

def update_curve_results(curve, curve_function, params_global, params_local_names, order_bound, results, logfile):
    feedback("Processing curve " + curve.name + ":", outfile = logfile, newlines = 1)
    if not curve.name in results:
        results[curve.name] = {}

    if curve.nbits > order_bound:
        feedback("Too large order\n", outfile = logfile)
        return results[curve.name]

    for params_local_values in itertools.product(*params_global.values()):
        params_local = dict(zip(params_local_names, params_local_values))
        feedback("\tProcessing params " + str(params_local), outfile = logfile, frmt = '{:.<60}')
        if str(params_local) in results[curve.name]:
            feedback("Already computed", outfile = logfile, newlines = 1)
            continue
        else:
            results[curve.name][str(params_local)] = [curve_function(curve, params_local_names, *params_local_values)]
            feedback("Done", outfile = logfile, newlines = 1)
    return results[curve.name]

def compute_results(test_name, curve_function, params_global, params_local_names, order_bound = 256 , overwrite = False, curve_list = curves):
    jsonfile, tmpfile, logfile = handle_files(test_name)
    param_list = list(params_global.values())
    results = load_from_json(jsonfile)

    start_time = time.time()
    total_time = 0

    for curve in curve_list:
        results[curve.name] = update_curve_results(curve, curve_function, params_global, params_local_names, order_bound, results, logfile)
        save_into_json(results, tmpfile, 'w', indent = 1)

        end_time = time.time()
        diff_time = end_time - start_time
        total_time += diff_time

        feedback("Done, time elapsed: " + str(diff_time), outfile = logfile, newlines = 2)
        start_time = time.time()

    feedback(50  * '.' + "\n" + "Finished, total time elapsed: " + str(total_time), outfile = logfile) 
    os.remove(jsonfile)
    os.rename(tmpfile, jsonfile)

def pretty_print_results(test_name, result_names, captions, parameters, head = 2 **100 , curve_list = curves, res_sort_key = lambda x: x, curve_sort_key = "bits", save_to_txt = True):
    infile, _, _, outfile = init_test(test_name)
    results = load_from_json(infile)
    param_index = 0
    for i, pair in enumerate(list(results.values())[0]):
        if pair[0] == parameters:
            param_index = i
            break

    params = list(results.values())[0][param_index][0]
    param_table = PrettyTable(['parameter', 'value'])
    for param in params.keys():
        param_table.add_row([param, params[param]])
    print(param_table, '\n\n')
    
    assert len(result_names) == len(captions)
    cols = len(result_names)
    names_computed = results.keys()
    headlines = ['name', 'bits']
    for caption in captions:
        headlines.append(caption)
    t = PrettyTable(headlines)
    
    for curve in curve_list:
        name = curve.name
        order_bits = curve.nbits
        if name in names_computed:
            res_sorted = []
            for res in result_names:
                data = results[name][param_index][1]
                for r in res:
                    data = data[r]
                try:
                    res_sorted.append(sorted(data, key = res_sort_key)[:head])
                except TypeError as e:
                    res_sorted.append(data)
        else:
            res_sorted = ["Not computed"] * cols
        row = [name, order_bits]
        for res in res_sorted:
            row.append(res)
        t.add_row(row)
    t.sortby = curve_sort_key
    print(t)
    
    if save_to_txt:
        with open(outfile, "w") as f:
            f.write(str(param_table))
            f.write('\n\n')
            f.write(str(t))

#https://ask.sagemath.org/question/10112/kill-the-thread-in-a-long-computation/
def timeout(func, args=(), kwargs={}, timeout_duration = 10 ):
    @fork(timeout=timeout_duration, verbose=False)
    def my_new_func():
        return func(*args, **kwargs)
    return my_new_func()

def ints_before_strings(x):
    try:
        return ZZ(x)
    except:
        return oo

def remove_values_from_list(l, val):
    return [value for value in l if value != val]

# def parameter_gen(params_global_dic, cu_name):
#   var_names = params_global_dic.keys()
#   var_names_local = [var_name ar_name in var_names]
#   for ntuple in itertools.product(params_global_dic.values()):


# def delete_local_params_from_global(params_global, params_local):
#   '''Assumes that params_global is a dictionary of lists (without duplicities)'''
#   # assert len(list(params_global.keys())) == len(list((ast.literal_eval(params_local)).keys()))
#   local_keys = params_local.keys()
#   for local_key in local_keys:
#       local_key_dict = ast.literal_eval(local_key)
#       local_key_dict_keys = local_key_dict.keys()
#       for local_key_dict_key in local_key_dict_keys:
#           globname = str(local_key_dict_key) + "_globlist"
#           assert globname in params_global
#           local_value = local_key_dict[local_key_dict_key]
#           params_global[globname]=remove_values_from_list(params_global[globname], local_value)
#   return params_global