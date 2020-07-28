from curve_analyzer.definitions import CURVE_PATH
from curve_analyzer.utils.custom_curve import CustomCurve
from sage.all import ZZ
import json
import os
import re

def import_curve_db(root = CURVE_PATH, ignore_sim = True):
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
                if ignore_sim:
                    continue
                suffix = "-" + str(re.findall(r'\d+', file)[0 ])
            with open(os.path.join(path, file)) as f:
                curve_db[source + suffix] = json.load(f)
    return curve_db

def curve_gen(curve_db, curve_type, order_bound, verbose):
    sources = curve_db.keys()
    for source in sources:
        curves = curve_db[source]['curves']
        for curve in curves:
            if ZZ(curve['order']).nbits() > order_bound:
                continue
            name = curve['name']
            if curve_type == "std" and "sim" in name:
                continue
            if curve_type == "sim" and not "sim" in name:
                continue
            if curve_type == "sample" and not name in ["secp112r1", "secp192r1", "secp256r1"]:
                continue
            if verbose:
                print(curve['name'])
            yield CustomCurve(curve)

def custom_curves(curve_db, curve_type, order_bound, verbose):
    return [c for c in curve_gen(curve_db, curve_type, order_bound, verbose)]

def import_curves(curve_type = "sample", order_bound = 256, verbose = False):
    print("Importing " + curve_type + " curves of sizes up to " + str(order_bound) + " bits from the database...")
    ignore_sim = True
    if curve_type in ["sim", "all"]:
        ignore_sim = False
    curve_db = import_curve_db(CURVE_PATH, ignore_sim)
    curve_list = sorted(custom_curves(curve_db, curve_type, order_bound, verbose), key = lambda item: item.name)
    return curve_list