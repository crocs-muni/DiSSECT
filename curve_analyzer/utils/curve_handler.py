import json
import os

from sage.all import ZZ

from curve_analyzer.definitions import CURVE_PATH, CURVE_PATH_SIM
from curve_analyzer.utils.custom_curve import CustomCurve


# Generates a dictionary with keys = sources of curves (secg, gost,...) and values = dictionaries
# These dictionaries contain description and a list of all curves from corresponding source
# Curves must be in the folder CURVE_PATH (std) or SIM_CURVE_PATH (sim)
# The flag ignore_sim is used for ignoring simulated curves during importing
def import_curve_db(ignore_sim=True):
    curve_db = {}
    for path, dirs, files in os.walk(CURVE_PATH):
        if dirs != []:
            continue
        source = path.split("/")[-1]

        # import std curves
        for file in files:
            if os.path.splitext(file)[-1] != ".json":
                continue
            with open(os.path.join(path, file)) as f:
                curve_db[source] = json.load(f)

    if not ignore_sim:
        # import sim curves
        for path, dirs, files in os.walk(CURVE_PATH_SIM):
            if dirs != []:
                continue
            source = path.split("/")[-1]

            # import std curves
            for file in files:
                if os.path.splitext(file)[-1] != ".json":
                    continue
                with open(os.path.join(path, file)) as f:
                    curve_db[source] = json.load(f)
    return curve_db


# Yields instances of the class CustomCurve from the dictionary generated by import_curve_db
# Curves can be specified by order_bound or curve_type: simulated (sim), standard (std) or sample (smp)
def curve_gen(curve_db, curve_type, order_bound, verbose, binary, extension, single_curve, allowed_cofactors):
    sources = curve_db.keys()
    for source in sources:
        curves = curve_db[source]['curves']
        for curve in curves:
            if ZZ(curve["cofactor"]) not in [ZZ(c) for c in allowed_cofactors]:
                continue
            if not binary and curve["field"]["type"] == "Binary":
                continue
            if not extension and curve["field"]["type"] == "Extension":
                continue
            if single_curve != "" and curve["name"] != single_curve:
                continue
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


# Makes a list from the result of curve_gen
def custom_curves(curve_db, curve_type, order_bound, verbose, binary, extension, single_curve, allowed_cofactors):
    return [c for c in
            curve_gen(curve_db, curve_type, order_bound, verbose, binary, extension, single_curve, allowed_cofactors)]


# Creates a list of instances of class CustomCurve out of imported database (conditioned by curve_type, see above)
def import_curves(curve_type="sample", order_bound=256, verbose=False, binary=False, extension=False, single_curve="",
                  allowed_cofactors=None, chunk=1, chunks_total=1):
    if allowed_cofactors is None:
        allowed_cofactors = [1]
    assert chunk <= chunks_total

    if single_curve != "":
        print("Importing " + single_curve)
    else:
        print("Importing " + curve_type + " curves of sizes up to " + str(
            order_bound) + " bits from the database, allowed cofactors: " + str(allowed_cofactors))
    ignore_sim = True
    if curve_type in ["sim", "all"]:
        ignore_sim = False
    curve_db = import_curve_db(ignore_sim)
    curve_list = sorted(
        custom_curves(curve_db, curve_type, order_bound, verbose, binary, extension, single_curve, allowed_cofactors),
        key=lambda item: item.order)
    if verbose:
        print("")

    def chunkify(lst, n):
        """Split lst into n chunks"""
        return [lst[i::n] for i in range(n)]

    curve_chunks = chunkify(curve_list, chunks_total)
    return curve_chunks[chunk - 1]


def filter_curve_names(
        allowed_categories=None, allowed_bitsizes=range(257), allowed_cofactors=None, allow_binary=False,
        allow_extension=False):
    if allowed_cofactors is None:
        allowed_cofactors = [1]
    if allowed_categories is None:
        allowed_categories = ["nist", "x962", "x962_sim_128", "x962_sim_160", "x962_sim_192", "x962_sim_224",
                              "x962_sim_256"]
    ignore_sim = not any('sim' in cat for cat in allowed_categories)
    curve_db = import_curve_db(ignore_sim=ignore_sim)

    curve_names = []
    sources = curve_db.keys()
    for source in sources:
        curves = curve_db[source]["curves"]
        for curve in curves:
            if curve["category"] in allowed_categories and ZZ(curve["cofactor"]) in [ZZ(c) for c in
                                                                                     allowed_cofactors] and \
                    curve["field"]["bits"] in allowed_bitsizes:
                if (allow_binary == False and curve["field"]["type"] == "Binary") or (
                        allow_extension == False and curve["field"]["type"] == "Extension"):
                    continue
                curve_names.append(curve["name"])
    return curve_names


def filter_results(json_file,
                   allowed_categories=None, allowed_bitsizes=range(257), allowed_cofactors=None,
                   allow_binary=False, allow_extension=False):
    if allowed_cofactors is None:
        allowed_cofactors = [1]
    if allowed_categories is None:
        allowed_categories = ["nist", "x962", "x962_sim_128", "x962_sim_160", "x962_sim_192", "x962_sim_224",
                              "x962_sim_256"]
    curve_names = filter_curve_names(allowed_categories=allowed_categories, allowed_bitsizes=allowed_bitsizes,
                                     allowed_cofactors=allowed_cofactors, allow_binary=allow_binary,
                                     allow_extension=allow_extension)
    with open(json_file, 'r') as rf:
        results = json.load(rf)
        for key in list(results):
            if key not in curve_names:
                del results[key]
        return results
