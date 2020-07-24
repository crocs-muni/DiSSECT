from curve_analyzer.definitions import CURVE_PATH
from curve_analyzer.utils.custom_curve import CustomCurve
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

def curve_gen(curve_db):
    sources = curve_db.keys()
    for source in sources:
        curves = curve_db[source]['curves']
        for curve in curves:
            yield CustomCurve(curve)

def custom_curves(curve_db):
    return [c for c in curve_gen(curve_db)]

def custom_curves_sorted_by_name(curve_db):
    return sorted(custom_curves(curve_db), key = lambda item: item.name)

# def init_curve_db():
print("importing database")
curve_db = import_curve_db(CURVE_PATH)
curves = sorted(custom_curves(curve_db))
curves_sample = [c for c in curves if c.name in ["secp112r1", "secp192r1", "secp256r1"]]
curves_sim = [c for c in curves if "sim" in c.name]
curves_std = [c for c in curves if not "sim" in c.name]
