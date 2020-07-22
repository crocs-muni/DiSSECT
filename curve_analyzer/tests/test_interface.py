from sage.all_cmdline import *   # import sage library
from curve_analyzer.utils.json_handler import *
from curve_analyzer.definitions import TEST_PATH
from prettytable import PrettyTable  # http://zetcode.com/python/prettytable/
from collections import OrderedDict
from datetime import datetime
import time
import pytz
import itertools
import os
import ast

def get_timestamp():
    cest = pytz.timezone('Europe/Prague')
    now = datetime.now()
    now = cest.localize(now)
    return datetime.isoformat(now, sep = '_', timespec = 'seconds')[:-6]

class Logs:
    def __init__(self, test_name, desc = ''):
        self.desc = desc
        self.init_log_paths(test_name)
        self.create_logs(test_name)

    def init_log_paths(self, test_name):
        self.main_log_file = TEST_PATH + '/' + test_name + '/' + test_name + ".log"
        self.log_dir = TEST_PATH + '/' + test_name + '/logs/'
        timestamp = get_timestamp()
        if not self.desc == '':
            name = timestamp + "_" + self.desc
        else:
            name = timestamp
        self.current_log_file = self.log_dir + name + '.log'

    def create_logs(self, test_name):
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)
        if not os.path.exists(self.main_log_file):
            with open(self.main_log_file, 'w'):
                pass
        self.main_log = open(self.main_log_file, 'a')
        self.current_log = open(self.current_log_file, 'w')

    def write_to_logs(self, text, frmt = '{:s}', newlines = 0):
        print(frmt.format(text), end = newlines * "\n")
        for f in [self.main_log, self.current_log]:
            f.write(frmt.format(text))
            f.write(newlines * "\n")

    def close_logs(self):
        for f in [self.main_log, self.current_log]:
            f.close()
   
def init_json_paths(test_name):
    path_json = TEST_PATH + '/' + test_name + '/' + test_name + '.json'
    path_tmp = TEST_PATH + '/' + test_name + '/' + 'tmp.json'
    if not os.path.exists(path_json):
        save_into_json({}, path_json, 'w')
    return path_json, path_tmp

def update_curve_results(curve, curve_function, params_global, params_local_names, order_bound, results, log_obj):
    log_obj.write_to_logs("Processing curve " + curve.name + ":", newlines = 1)
    if not curve.name in results:
        results[curve.name] = {}

    if curve.nbits > order_bound:
        log_obj.write_to_logs("Too large order\n")
        return results[curve.name]

    for params_local_values in itertools.product(*params_global.values()):
        params_local = dict(zip(params_local_names, params_local_values))
        log_obj.write_to_logs("\tProcessing params " + str(params_local), frmt = '{:.<60}')
        if str(params_local) in results[curve.name]:
            log_obj.write_to_logs("Already computed", newlines = 1)
            continue
        else:
            results[curve.name][str(params_local)] = curve_function(curve, *params_local_values)
            log_obj.write_to_logs("Done", newlines = 1)
    return results[curve.name]

def compute_results(test_name, curve_function, params_global, params_local_names, order_bound = 256, overwrite = False, curve_list = None, desc = ''):
    json_file, tmp_file = init_json_paths(test_name)
    log_obj = Logs(test_name, desc)
    param_list = list(params_global.values())
    results = load_from_json(json_file)
    
    total_time = 0
    timestamp = get_timestamp()

    log_obj.write_to_logs("Current datetime: " + timestamp, newlines = 1)
    std_count = 0
    sim_count = 0
    for curve in curve_list:
        if "sim" in curve.name:
            sim_count +=1
        else:
            std_count +=1
    log_obj.write_to_logs("Running test " + str(test_name) + " on " + str(std_count) + " std curves and " + str(sim_count) + " sim curves with global parameters:\n" + str(params_global), newlines = 2)


    for curve in curve_list:
        start_time = time.time()

        results[curve.name] = update_curve_results(curve, curve_function, params_global, params_local_names, order_bound, results, log_obj)

        end_time = time.time()
        diff_time = end_time - start_time
        total_time += diff_time

        log_obj.write_to_logs("Done, time elapsed: " + str(diff_time), newlines = 2)
        save_into_json(results, tmp_file, 'w', indent = 1)

    log_obj.write_to_logs(80  * '.' + "\n" + "Finished, total time elapsed: " + str(total_time) + "\n\n" + 80  * '#', newlines = 3) 
    os.remove(json_file)
    os.rename(tmp_file, json_file)

def init_txt_paths(test_name, desc = ''):
    name = TEST_PATH + '/' + test_name + '/' + test_name 
    if not desc == '':
        name += "_" + desc    
    return name + '.txt'

def pretty_print_results(test_name, get_captions, select_results, curve_list = None, curve_sort_key = "bits", save_to_txt = True):
    path_json, _ = init_json_paths(test_name)
    results = load_from_json(path_json)

    captions = get_captions(results)
    headlines = ['name', 'bits']
    for caption in captions:
        headlines.append(caption)
    t = PrettyTable(headlines)
    
    for curve in curve_list:
        name = curve.name
        if not name in results.keys():
            continue
        order_bits = curve.nbits
        row = [name, order_bits]
        for result in select_results(results[name].values()):
            row.append(result)
        t.add_row(row)

    t.sortby = curve_sort_key
    print(t)
    
    if save_to_txt:
        path_txt = init_txt_paths(test_name)
        with open(path_txt, "w") as f:
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
