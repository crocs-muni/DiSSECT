from sage.all_cmdline import *   # import sage library
from curve_analyzer.definitions import ROOT_DIR, CURVE_PATH, TEST_PATH

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

def curve_gen(curve_db):
    sources = curve_db.keys()
    for source in sources:
        curves = curve_db[source]['curves']
        for curve in curves:
            yield curve

def custom_curve_gen(curve_db):
    for db_curve in curve_gen(curve_db):
        curve = CustomCurve(db_curve)
        yield curve

def custom_curves(curve_db):
    return [c for c in custom_curve_gen(curve_db)]

def custom_curves_sorted_by_name(curve_db):
    return sorted(custom_curves(curve_db), key = lambda item: item.name)

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

