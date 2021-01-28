import itertools
import json
import random
import time
from datetime import datetime
from pathlib import Path

import pytz
from sage.all import sage_eval
from sage.parallel.decorate import fork

from curve_analyzer.definitions import TRAIT_PATH
from curve_analyzer.utils.json_handler import save_into_json, load_from_json


def get_timestamp():
    """Returns the current datetime as CEST."""
    cest = pytz.timezone('Europe/Prague')
    now = datetime.now()
    now = cest.localize(now)
    return datetime.isoformat(now, sep='_', timespec='seconds')[:-6]


class Logs:
    """Class for managing logs for each curve trait."""

    def __init__(self, trait_name, desc=''):
        self.desc = desc
        self.main_log_file = None
        self.main_log = None
        self.log_dir = None
        self.current_log_file = None
        self.current_log = None
        self.init_log_paths(trait_name)
        self.create_logs()

    def init_log_paths(self, trait_name):
        self.main_log_file = Path(TRAIT_PATH, trait_name, trait_name + ".log")
        self.log_dir = Path(TRAIT_PATH, trait_name, 'logs')
        timestamp = get_timestamp()
        if not self.desc == '':
            name = timestamp + "_" + self.desc
        else:
            name = timestamp
        self.current_log_file = Path(self.log_dir, name + '.log')

    def create_logs(self):
        self.log_dir.mkdir(exist_ok=True)
        self.main_log = open(self.main_log_file, 'a+')
        self.current_log = open(self.current_log_file, 'w')

    def write_to_logs(self, text, frmt='{:s}', newlines=0, verbose_print=False):
        if verbose_print:
            print(frmt.format(text), end=newlines * "\n")
        for f in [self.main_log, self.current_log]:
            f.write(frmt.format(text))
            f.write(newlines * "\n")

    def close_logs(self):
        for f in [self.main_log, self.current_log]:
            f.close()


def init_json_paths(trait_name, desc=''):
    """Deduces paths to JSON files from the trait name."""
    path_main_json = Path(TRAIT_PATH, trait_name, trait_name + '.json')
    path_json = Path(TRAIT_PATH, trait_name, trait_name + '_' + desc + '_' + get_timestamp() + '.json')
    # tmp name must be unique for parallel trait runs
    path_tmp = Path("%s_%04x.tmp" % (path_json.with_suffix(''), random.randrange(2 ** 32)))
    path_params = Path(TRAIT_PATH, trait_name, trait_name + '.params')
    if not path_json.is_file():
        save_into_json({}, path_json, 'w')
    return path_main_json, path_json, path_tmp, path_params


def special_case(text):
    if not isinstance(text, str):
        return False
    return text.strip() == "NO DATA (timed out)"


def compare_structures(struct1, struct2):
    if type(struct1) != type(struct2):
        if special_case(struct1) or special_case(struct2):
            return True
        return False
    if isinstance(struct1, list):
        value = True
        for i in range(min(len(struct1), len(struct2))):
            value &= compare_structures(struct1[i], struct2[i])
        return value
    if isinstance(struct1, dict):
        if set(struct1.keys()) != set(struct2.keys()):
            return False
        value = True
        for key in struct1.keys():
            value &= compare_structures(struct1[key], struct2[key])
        return value
    return True


def get_model_structure(curve_function):
    name = curve_function.__name__.split("_", 1)[0]
    with open(Path(TRAIT_PATH, name, name + "_structure.json"), 'r') as f:
        results = json.load(f)
    return list(list(results.values())[0].values())[0]


def is_structure_new(old, curve_function, curve):
    if curve.name not in old:
        return True
    model_structure = get_model_structure(curve_function)
    computed = list(old[curve.name].values())[0]
    return not compare_structures(model_structure, computed)


def update_curve_results(curve, curve_function, params_global, params_local_names, old_results, log_obj, verbose=False):
    """Tries to run traits for each individual curve; called by compute_results."""
    log_obj.write_to_logs("Processing curve " + curve.name + ":", newlines=1, verbose_print=verbose)
    new_results = {}
    new_struct = is_structure_new(old_results, curve_function, curve)
    if curve.name not in old_results:
        new_results[curve.name] = {}
    else:
        new_results[curve.name] = old_results[curve.name]

    for params_local_values in itertools.product(*params_global.values()):
        params_local = dict(zip(params_local_names, params_local_values))
        log_obj.write_to_logs("    Processing params " + str(params_local), frmt='{:.<107}', verbose_print=verbose)
        if curve.name in old_results and str(params_local) in old_results[curve.name] and not new_struct:
            log_obj.write_to_logs("Already computed", newlines=1, verbose_print=verbose)
        else:
            new_results[curve.name][str(params_local)] = curve_function(curve, *params_local_values)
            log_obj.write_to_logs("Done", newlines=1, verbose_print=verbose)
    return new_results[curve.name]


def compute_results(curve_list, trait_name, curve_function, desc='', verbose=False):
    """A universal function for running traits on curve lists; it is called by each trait file which has its own curve
    function. Each trait is assumed to have a params file in its folder; the results and logs are created there as
    well. """
    main_json_file, json_file, tmp_file, params_file = init_json_paths(trait_name, desc)
    if curve_list == []:
        print("No input curves found, terminating the trait run.")
        save_into_json({}, json_file, 'w')
        return
    log_obj = Logs(trait_name, desc)
    try:
        old_results = load_from_json(main_json_file)
    except FileNotFoundError:
        old_results = {}

    new_results = {}
    if not params_file.is_file():
        print("No parameter file found, terminating the trait run.")
        return
    params = load_from_json(params_file)
    for key in params["params_global"].keys():
        params["params_global"][key] = sage_eval(params["params_global"][key])
    params_global = params["params_global"]
    params_local_names = params["params_local_names"]

    total_time = 0
    timestamp = get_timestamp()

    log_obj.write_to_logs("Current datetime: " + timestamp, newlines=1, verbose_print=verbose)
    std_count = 0
    sim_count = 0
    for curve in curve_list:
        if "sim" in curve.name:
            sim_count += 1
        else:
            std_count += 1
    log_obj.write_to_logs(
        "Hold on to your hat! Running trait " + str(trait_name) + " on " + str(std_count) + " std curves and " + str(
            sim_count) + " sim curves with global parameters:\n" + str(params_global), newlines=2,
        verbose_print=verbose)

    for curve in curve_list:
        start_time = time.time()

        new_results[curve.name] = update_curve_results(curve, curve_function, params_global, params_local_names,
                                                       old_results, log_obj, verbose=verbose)

        end_time = time.time()
        diff_time = end_time - start_time
        total_time += diff_time

        log_obj.write_to_logs("Done, time elapsed: " + str(diff_time), newlines=2, verbose_print=verbose)
        save_into_json(new_results, tmp_file, 'w')

    log_obj.write_to_logs(80 * '.' + "\n" + "Finished, total time elapsed: " + str(total_time) + "\n\n" + 80 * '#',
                          newlines=3, verbose_print=verbose)
    log_obj.close_logs()

    json_file.unlink()
    tmp_file.rename(json_file)


def timeout(func, args=(), kwargs=None, timeout_duration=10):
    """Stops the function func after 'timeout_duration' seconds, taken from
    https://ask.sagemath.org/question/10112/kill-the-thread-in-a-long-computation/. """
    if kwargs is None:
        kwargs = {}

    @fork(timeout=timeout_duration, verbose=False)
    def my_new_func():
        return func(*args, **kwargs)

    return my_new_func()
