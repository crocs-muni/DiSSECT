from sage.all_cmdline import *   # import sage library
from curve_analyzer.definitions import ROOT_DIR, CURVE_PATH, FILTER_PATH, TEST_PATH

import os
import time
import sys
import fnmatch
import hashlib
import re
from prettytable import PrettyTable
# http://zetcode.com/python/prettytable/

def import_curve_db(root = CURVE_PATH):
    curve_db = {}
    for path, dirs, files in os.walk(root):
        if dirs != [] and '.ipynb_checkpoints' not in dirs:
            continue
        source = path.split("/")[-1 ]
        suffix = ""
        for file in files:
            if os.path.splitext(file)[-1 ] != ".json":
                continue

            if "sim" in path:
                suffix = "-" + str(re.findall(r'\d+', file)[0 ])
            with open(os.path.join(path, file)) as f:
                curve_db[source + suffix] = json.load(f)
    return curve_db

# sources = ['anssi', 'bls', 'bn', 'brainpool', 'gost', 'mnt', 'nist', 'other', 'secg', 'x962']
#114 curves in total, 83 unique orders

def count_curves(curve_db):
    total = 0 
    sources = curve_db.keys()
    for source in sources:
        count = len(curve_db[source]['curves'])
        total += count
        print(source, count)
    return total

def filter_out_sources(curve_db, filtering_source_list, filtering_curve_list):
    filtered_curve_db = {}
    sources = curve_db.keys()
    for source in sources:
        if not any(word in source for word in filtering_source_list):
            filtered_curve_db[source] = curve_db[source]
    return filtered_curve_db

def get_exact_duplicities(curve_db, verbose = False):
    sources = curve_db.keys()
    duplicities = []
    for source in sources:
        for curve in curve_db[source]['curves']:
            try:
                aliases = curve['aliases']
                name = source + '/' + curve['name']
                if verbose:
                    print(name + ": ", aliases)
                if not name in duplicities:
                    for string in aliases:
                        if not string in duplicities:
                            duplicities.append(string)
            except:
                continue
    return duplicities
            
def get_orders(curve_db):
    orders = []
    sources = curve_db.keys()
    for source in sources:
         for curve in curve_db[source]['curves']:
                order = ZZ(curve['order'])
                orders.append(order)
    return orders

def curve_gen(curve_db):
    sources = curve_db.keys()
    for source in sources:
        curves = curve_db[source]['curves']
        for curve in curves:
            yield curve

def write_list_to_file(l, fname = "test.txt"):
    with open(fname, 'w') as f:
        f.write(str(l))


def bitlen_sorted_names_gen():
    l = load_from_json(FILTER_PATH)
    sorted_orders = sorted(l.keys(), key = lambda x: ZZ(x))
    sorted_names = [l[o] for o in sorted_orders]
    for name in sorted_names:
        yield name

def custom_curve_gen(curve_db):
    for db_curve in curve_gen(curve_db):
        curve = CustomCurve(db_curve)
        yield curve

def custom_curves(curve_db):
    return [c for c in custom_curve_gen(curve_db)]

def custom_curves_sorted_by_name(curve_db):
    return sorted(custom_curves(curve_db), key = lambda item: item.name)

def bitlen_sorted_custom_curve_gen():
    l = load_from_json('/home/x408178/Research/Curve_checker/filters/ord_to_name.json')
    sorted_orders = sorted(l.keys(), key = lambda x: ZZ(x))
    sorted_names = [l[o] for o in sorted_orders]
    for name in sorted_names:
        yield name

def embedding_degree_q(q, r):
    '''returns embedding degree with respect to q'''
    return Mod(q,r).multiplicative_order()

def embedding_degree(E, r):
    '''returns relative embedding degree with respect to E'''
    q = (E.base_field()).order()
    return embedding_degree_q(q, r)

try:
    curve_db
except NameError:
    curve_db = import_curve_db(CURVE_PATH)

try:
    curves
except NameError:
    curves = sorted(custom_curves(curve_db))

try:
    curves_sample
except NameError:
    curves_sample = [c for c in curves if c.name in ["secp112r1", "secp192r1", "secp256r1"]]

try:
    curves_sim
except NameError:
    curves_sim = [c for c in curves if "sim" in c.name]

try:
    curves_std
except NameError:
    curves_std = [c for c in curves if not "sim" in c.name]

