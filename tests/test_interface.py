from sage.all_cmdline import *   # import sage library
from curve_analyzer.utils.curve_handler import *
from curve_analyzer.utils.json_handler import *
from curve_analyzer.definitions import ROOT_DIR, CURVE_PATH, TEST_PATH
from prettytable import PrettyTable   # http://zetcode.com/python/prettytable/
import time

def init_test(test_name):
    path_json = TEST_PATH + '/' + test_name + '/' + test_name + '.json'
    path_log = os.path.splitext(path_json)[0 ] + ".log"
    path_txt = os.path.splitext(path_json)[0 ] + ".txt"
    return path_json, path_log, path_txt

#https://ask.sagemath.org/question/10112/kill-the-thread-in-a-long-computation/
def timeout(func, args=(), kwargs={}, timeout_duration = 10 ):
    @fork(timeout=timeout_duration, verbose=False)
    def my_new_func():
        return func(*args, **kwargs)
    return my_new_func()

def compute_results(test_name, curve_function, parameters, order_bound = 256 , overwrite = False, curve_list = curves):
    jsonfile, logfile, _ = init_test(test_name)
    if os.path.exists(jsonfile) and not overwrite:
        print("The result file already exists! Aborting...")
        return
    def feedback(text, frmt = '{:s}', outfile = logfile):
        print(frmt.format(text), end = '')
        with open(outfile, 'a') as f:
            f.write(frmt.format(text))
    with open(logfile, 'w'):
        pass

    total = {'parameters': {}, 'results': {}}
    total['parameters'] = parameters
    param_list = list(parameters.values())
    results = {}

    start_time = time.time()
    total_time = 0 

    for curve in curve_list:
        feedback("Processing curve " + curve.name, '{:.<60}')
        
        if curve.order.nbits() > order_bound:
            feedback("Too large order\n")
            continue

        results[curve.name] = curve_function(curve, *param_list)

        end_time = time.time()
        diff_time = end_time - start_time
        total_time += diff_time

        feedback("Done, time elapsed: " + str(diff_time) + "\n")
        
        total['results'] = results
        save_into_json(total, jsonfile, 'w')
        start_time = time.time()
    feedback(90  * '.' + "\n" + "Finished, total time elapsed: " + str(total_time))

def pretty_print_results(test_name, result_names, captions, head = 2 **100 , curve_list = curves, res_sort_key = lambda x: x, curve_sort_key = "bits", save_to_txt = True):
    infile, _, outfile = init_test(test_name)
    total = load_from_json(infile)
    params = total['parameters']
    param_table = PrettyTable(['parameter', 'value'])
    for param in params.keys():
        param_table.add_row([param, params[param]])
    print(param_table, '\n\n')
    
    assert len(result_names) == len(captions)
    cols = len(result_names)
    results = total['results']
    names_computed = results.keys()
    headlines = ['name', 'bits']
    for caption in captions:
        headlines.append(caption)
    t = PrettyTable(headlines)
    
    for curve in curve_list:
        name = curve.name
        order_bits = curve.order.nbits()
        if name in names_computed:
            res_sorted = []
            for res in result_names:
                data = results[name]
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

def ints_before_strings(x):
    try:
        return ZZ(x)
    except:
        return oo

def remove_values_from_list(l, val):
    return [value for value in l if value != val]

