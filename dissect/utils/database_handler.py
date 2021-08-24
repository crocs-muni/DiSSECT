#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Optional, Tuple, Iterable, Dict, Any

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError
from sage.all import Integer

from dissect.utils.custom_curve import CustomCurve
from dissect.traits.trait_info import TRAIT_INFO


def connect(database: Optional[str] = None) -> Database:
    client = MongoClient(database, connect=False)
    return client["dissect"]


def create_curves_index(db: Database) -> None:
    db["curves"].create_index([("name", 1)], unique=True)


def create_trait_index(db: Database, trait: str) -> None:
    db[f"trait_{trait}"].create_index([("curve", 1), ("params", 1)], unique=True)


def _format_curve(curve):
    c = dict()
    c["name"] = curve["name"]
    c["category"] = curve["category"]
    if curve.get("aliases"):
        c["aliases"] = curve["aliases"]
    if curve.get("oid"):
        c["oid"] = curve["oid"]
    if curve.get("desc"):
        c["desc"] = curve["desc"]
    c["form"] = curve["form"]
    c["field"] = curve["field"]
    c["params"] = curve["params"]
    try:
        if (curve["generator"]["x"]["raw"] or curve["generator"]["x"]["poly"]) and (
                curve["generator"]["y"]["raw"] or curve["generator"]["y"]["poly"]):
            c["generator"] = curve["generator"]
    except:
        pass

    if isinstance(curve["order"], int):
        c["order"] = hex(curve["order"])
    elif isinstance(curve["order"], str):  # Workaround for std database
        c["order"] = hex(int(curve["order"], base=16))

    if isinstance(curve["cofactor"], int):
        c["cofactor"] = hex(curve["cofactor"])
    elif isinstance(curve["cofactor"], str):  # Workaround for std database
        c["cofactor"] = hex(int(curve["cofactor"], base=16))

    c["standard"] = False if "sim" in curve["category"] else True
    c["example"] = curve.get("example", False)

    if curve.get("simulation"):
        sim = curve["simulation"]
    else:
        sim = {}
        if "seed" in curve and curve["seed"]:
            sim["seed"] = hex(int(curve["seed"], base=16))
        elif "characteristics" in curve and "seed" in curve["characteristics"] and curve["characteristics"]["seed"]:
            sim["seed"] = hex(int(curve["characteristics"]["seed"], base=16))

    if sim:
        c["simulation"] = sim

    if curve.get("properties"):
        properties = curve["properties"]
    else:
        properties = {}

    if properties:
        c["properties"] = properties

    return c


def upload_curves(db: Database, path: str) -> Tuple[int, int]:
    try:
        with open(path, "r") as f:
            curves = json.load(f)

        if not isinstance(
                curves, list
        ):  # inconsistency between simulated and standard format
            curves = curves["curves"]
    except Exception:  # invalid format
        return 0, 0

    success = 0
    for curve in curves:
        try:
            if db["curves"].insert_one(_format_curve(curve)):
                success += 1
        except DuplicateKeyError:
            pass

    return success, len(curves)


def upload_results(db: Database, trait_name: str, path: str) -> Tuple[int, int]:
    try:
        with open(path, "r") as f:
            results = json.load(f)
    except Exception:  # invalid format
        return 0, 0

    success = 0
    total = 0
    for result in results:
        total += 1

        record = {}
        try:
            if isinstance(result["curve"], str):
                curve = db["curves"].find_one({"name": result["curve"]})
                record["curve"] = {}
                record["curve"]["name"] = curve["name"]
                record["curve"]["standard"] = curve["standard"]
                record["curve"]["example"] = curve["example"]
                record["curve"]["category"] = curve["category"]
                record["curve"]["bits"] = curve["field"]["bits"]
                record["curve"]["field_type"] = curve["field"]["type"]
                record["curve"]["cofactor"] = curve["cofactor"]
            else:
                record["curve"] = result["curve"]
            record["params"] = result["params"]
            record["result"] = result["result"]

            if db[f"trait_{trait_name}"].insert_one(record):
                success += 1
        except Exception:
            pass

    return success, total


def get_curves_old(
        db: Database, filters: Any = {}, raw: bool = False
) -> Iterable[CustomCurve]:
    curve_filter: Dict[str, Any] = {}

    # Curve type filter
    if hasattr(filters, "curve_type"):
        if filters.curve_type == "sim":
            curve_filter["standard"] = False
        elif filters.curve_type == "std":
            curve_filter["standard"] = True
        elif filters.curve_type != "all":
            curve_filter["category"] = filters.curve_type

    # Bit-length filter
    if hasattr(filters, "order_bound") and filters.order_bound != 0:
        curve_filter["field.bits"] = {"$lte": filters.order_bound}

    # Cofactor filter
    if hasattr(filters, "allowed_cofactors") and filters.allowed_cofactors:
        curve_filter["cofactor"] = {"$in": list(map(hex, filters.allowed_cofactors))}

    cursor = db.curves.aggregate([{"$match": curve_filter}])

    if raw:
        return map(_decode_ints, cursor)
    # Cursor tends to timeout -> collect the results first (memory heavy), alternatively disable cursor timeout
    return map(CustomCurve, list(cursor))

def get_curves(db: Database, query: Any = None) -> Iterable[CustomCurve]:
    aggregate_pipeline = []
    aggregate_pipeline.append({"$match": format_curve_query(query) if query else dict()})
    aggregate_pipeline.append({"$unset": "_id"})
    curves = list(db["curves"].aggregate(aggregate_pipeline))

    return map(_decode_ints, curves)

def get_curve_categories(db: Database) -> Iterable[str]:
    return db["curves"].distinct("category")

def format_curve_query(query: Dict[str, Any]) -> Dict[str, Any]:
    result = {}

    def helper(key, cast, db_key = None):
        if key not in query:
            return

        db_key = db_key if db_key else key

        if isinstance(query[key], list):
            if len(query[key]) == 0 or "all" in query[key]:
                return
            if len(query[key]) == 1:
                result[db_key] = cast(query[key][0])
            else:
                result[db_key] = { "$in": list(map(cast, query[key])) }
        elif query[key] != "all":
            result[db_key] = cast(query[key])

    helper("name", str)
    helper("standard", bool)
    helper("example", bool)
    helper("category", str)
    helper("bits", int, "field.bits")
    helper("cofactor", int)
    helper("field_type", str, "field.type")

    return result


def _cast_sage_types(result: Any) -> Any:
    if isinstance(result, Integer):
        return int(result)

    if isinstance(result, dict):
        for key, value in result.items():
            result[key] = _cast_sage_types(value)
    elif isinstance(result, list):
        for idx, value in enumerate(result):
            result[idx] = _cast_sage_types(value)

    return result


def _encode_ints(result: Any) -> Any:
    if isinstance(result, Integer) or isinstance(result, int):
        return hex(result)
    if isinstance(result, dict):
        for key, value in result.items():
            result[key] = _encode_ints(value)
    elif isinstance(result, list):
        for idx, value in enumerate(result):
            result[idx] = _encode_ints(value)

    return result


def store_trait_result(
        db: Database,
        curve: CustomCurve,
        trait: str,
        params: Dict[str, Any],
        result: Dict[str, Any],
) -> bool:
    trait_result = {}
    trait_result["curve"] = {}
    trait_result["curve"]["name"] = curve.name()
    trait_result["curve"]["standard"] = curve.standard()
    trait_result["curve"]["example"] = curve.example()
    trait_result["curve"]["category"] = curve.category()
    trait_result["curve"]["bits"] = curve.q().nbits()
    trait_result["curve"]["cofactor"] = curve.cofactor()
    trait_result["curve"] = _cast_sage_types(trait_result["curve"])
    trait_result["params"] = _cast_sage_types(params)
    trait_result["result"] = _encode_ints(result)
    try:
        return db[f"trait_{trait}"].insert_one(trait_result).acknowledged
    except DuplicateKeyError:
        return False


def is_solved(
        db: Database, curve: CustomCurve, trait: str, params: Dict[str, Any]
) -> bool:
    trait_result = {"curve": curve.name()}
    trait_result["params"] = _cast_sage_types(params)
    return db[f"trait_{trait}"].find_one(trait_result) is not None


def get_trait_results(
        db: Database,
        trait: str,
        query: Dict[str, Any] = None,
        limit: int = None
):
    aggregate_pipeline = []
    aggregate_pipeline.append({"$match": format_trait_query(trait, query) if query else dict()})
    aggregate_pipeline.append({"$unset": "_id"})
    if limit:
        aggregate_pipeline.append({"$limit": limit})

    aggregated = list(db[f"trait_{trait}"].aggregate(aggregate_pipeline))
    return map(_decode_ints, map(_flatten_trait_result, aggregated))

def format_trait_query(trait_name: str, query: Dict[str, Any]) -> Dict[str, Any]:
    result = {}

    def helper(key, cast, db_key = None):
        if key not in query:
            return

        db_key = db_key if db_key else key

        if isinstance(query[key], list):
            if len(query[key]) == 0 or "all" in query[key]:
                return
            if len(query[key]) == 1:
                result[db_key] = cast(query[key][0])
            else:
                result[db_key] = { "$in": list(map(cast, query[key])) }
        elif query[key] != "all":
            result[db_key] = cast(query[key])

    helper("name", str, "curve.name")
    helper("standard", bool, "curve.standard")
    helper("example", bool, "curve.example")
    helper("category", str, "curve.category")
    helper("bits", int, "curve.bits")
    helper("cofactor", lambda x: hex(int(x)), "curve.cofactor")
    helper("field_type", str, "curve.field_type")

    for key in TRAIT_INFO[trait_name]["input"]:
        helper(key, TRAIT_INFO[trait_name]["input"][key][0], f"params.{key}")

    for key in TRAIT_INFO[trait_name]["output"]:
        helper(key, lambda x: _encode_ints(TRAIT_INFO[trait_name]["output"][key][0](x)), f"result.{key}")

    return result



# TODO move to data_processing?
def _flatten_trait_result(record: Dict[str, Any]):
    output = dict()

    _flatten_trait_result_rec(record["curve"], "", output)
    _flatten_trait_result_rec(record["params"], "", output)
    _flatten_trait_result_rec(record["result"], "", output)
    output["curve"] = output["name"]
    del output["name"]

    return output


def _flatten_trait_result_rec(
        record: Dict[str, Any], prefix: str, output: Dict[str, Any]
):
    for key in record:
        if isinstance(record[key], dict):
            _flatten_trait_result_rec(record[key], key + "_", output)
        else:
            output[prefix + key] = record[key]


def _decode_ints(source: Any) -> Any:
    if isinstance(source, str) and (source[:2].lower() == "0x" or source[:3].lower() == "-0x"):
        return int(source, base=16)
    if isinstance(source, dict):
        for key, value in source.items():
            source[key] = _decode_ints(value)
    elif isinstance(source, list):
        for idx, value in enumerate(source):
            source[idx] = _decode_ints(value)
    return source


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3 or not sys.argv[1] in ("curves", "results"):
        print(
            f"USAGE: python3 {sys.argv[0]} curves [database_uri] <curve_files...>",
            file=sys.stderr,
        )
        print(
            f"   OR: python3 {sys.argv[0]} results [database_uri] <trait_name> <results_file>",
            file=sys.stderr,
        )
        sys.exit(1)

    database_uri = "mongodb://localhost:27017/"
    args = sys.argv[2:]
    for idx, arg in enumerate(args):
        if "mongodb://" in arg:
            database_uri = arg
            del args[idx]
            break

    print(f"Connecting to database {database_uri}")
    db = connect(database_uri)


    def upload_curves_from_files(curve_files_list):
        for curves_file in curve_files_list:
            print(f"Loading curves from file {curves_file}")
            create_curves_index(db)
            uploaded, total = upload_curves(db, curves_file)
            print(f"Successfully uploaded {uploaded} out of {total}")


    def upload_results_from_file(trait_name, results_file):
        print(f"Loading trait {trait_name} results from file {results_file}")
        create_trait_index(db, trait_name)
        uploaded, total = upload_results(db, trait_name, results_file)
        print(f"Successfully uploaded {uploaded} out of {total}")


    if sys.argv[1] == "curves":
        upload_curves_from_files(args)
    elif sys.argv[1] == "results":
        upload_results_from_file(args[0], args[1])
