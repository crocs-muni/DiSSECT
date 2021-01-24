import json
from pathlib import Path
from typing import Optional, Tuple, Iterable, Dict, Any

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError
from sage.all import Integer

from curve_analyzer.definitions import CURVE_PATH, CURVE_PATH_SIM, TRAIT_NAMES, TRAIT_PATH
from curve_analyzer.utils.custom_curve import CustomCurve


def connect(database: Optional[str] = None) -> Database:
    client = MongoClient(database)
    return client["dissect"]


def create_curves_index(db: Database) -> None:
    db["curves"].create_index([("name", 1)], unique=True)


def create_trait_index(db: Database, trait: str) -> None:
    db[f"trait_{trait}"].create_index([("curve", 1), ("params", 1)], unique=True)


def upload_curves(db: Database, path: str) -> Tuple[int, int]:
    try:
        with open(path, "r") as f:
            curves = json.load(f)

        if not isinstance(curves, list):  # inconsistency between simulated and standard format
            curves = curves["curves"]
    except Exception:  # invalid format
        return 0, 0

    for curve in curves:
        curve["simulated"] = True if "sim" in curve["category"] else False
        if isinstance(curve["order"], int):
            curve["order"] = hex(curve["order"])

    success = 0
    for curve in curves:
        try:
            if db["curves"].insert_one(curve):
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
    for curve, result in results.items():
        for params, values in result.items():
            params = params.replace("'", '"')
            total += 1
            record = {
                "curve": curve,
                "params": json.loads(params),
                "result": _cast_sage_types(values)
            }
            try:
                if db[f"trait_{trait_name}"].insert_one(record):
                    success += 1
            except Exception:
                pass
    return success, total


def get_curves(db: Database, filters: Any = {}, raw: bool = False) -> Iterable[CustomCurve]:
    curve_filter: Dict[str, Any] = {}

    # Curve type filter
    if hasattr(filters, "curve_type"):
        if filters.curve_type == "sim":
            curve_filter["simulated"] = True
        elif filters.curve_type == "std":
            curve_filter["simulated"] = False
        elif filters.curve_type == "sample":
            curve_filter["simulated"] = False
            curve_filter["name"] = { "$in": ["secp112r1", "secp192r1", "secp256r1"] }
        elif filters.curve_type != "all":
            curve_filter["name"] = filters.curve_type

    # Bit-length filter
    if hasattr(filters, "order_bound"):
        curve_filter["field.bits"] = { "$lte": filters.order_bound }

    # Cofactor filter
    # TODO discuss if (allowed_cofactor == None => match_any) is ok
    if hasattr(filters, "allowed_cofactors") and filters.allowed_cofactors:
        curve_filter["cofactor"] = { "$in": list(map(int, filters.allowed_cofactors)) }

    cursor = db.curves.aggregate([
        { "$unset": "_id" },
        { "$match": curve_filter }
    ])

    if raw:
        return cursor
    # Cursor tends to timeout -> collect the results first (memory heavy), alternatively disable cursor timeout
    return map(CustomCurve, list(cursor))


# TODO this should be IMO handled by the traits - after finishing computation transform Sage values into Python values
def _cast_sage_types(result: Any) -> Any:
    if isinstance(result, int):
        return result if abs(result) < 2 ** 63 else hex(result)

    if isinstance(result, Integer):
        return _cast_sage_types(int(result))

    if isinstance(result, dict):
        for key, value in result.items():
            result[key] = _cast_sage_types(value)
    elif isinstance(result, list):
        for idx, value in enumerate(result):
            result[idx] = _cast_sage_types(value)

    return result


def store_trait_result(db: Database, curve: CustomCurve, trait: str, params: Dict[str, Any], result: Dict[str, Any]) -> bool:
    trait_result = { "curve": curve.name }
    trait_result["params"] = _cast_sage_types(params)
    trait_result["result"] = _cast_sage_types(result)
    try:
        return db[f"trait_{trait}"].insert_one(trait_result).acknowledged
    except DuplicateKeyError:
        return False


def is_solved(db: Database, curve: CustomCurve, trait: str, params: Dict[str, Any]) -> bool:
    trait_result = { "curve": curve.name }
    trait_result["params"] = _cast_sage_types(params)
    return db[f"trait_{trait}"].find_one(trait_result) is not None


def get_trait_results(db: Database, trait: str, params: Dict[str, Any] = None, curve: str = None, limit: int = None):
    result_filter = {}
    if params:
        result_filter["params"] = params
    if curve:
        result_filter["curve"] = { "$regex": curve }

    aggregate_pipeline = []
    aggregate_pipeline.append({ "$unset": "_id" })
    aggregate_pipeline.append({ "$match": result_filter })
    if limit:
        aggregate_pipeline.append({ "$limit": limit })

    return map(_flatten_trait_result, db[f"trait_{trait}"].aggregate(aggregate_pipeline))


def _flatten_trait_result(record: Dict[str, Any]):
    output = dict()

    output["curve"] = record["curve"]
    _flatten_trait_result_rec(record["params"], "", output)
    _flatten_trait_result_rec(record["result"], "", output)

    return output


def _flatten_trait_result_rec(record: Dict[str, Any], prefix: str, output: Dict[str, Any]):
    for key in record:
        if isinstance(record[key], dict):
            _flatten_trait_result(record[key], key + "_", output)
        else:
            output[prefix + key] = record[key]


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3 or not sys.argv[1] in ("curves", "results"):
        print(f"USAGE: python3 {sys.argv[0]} curves [database_uri] <curve_files...>", file=sys.stderr)
        print(f"   OR: python3 {sys.argv[0]} curves [database_uri] all", file=sys.stderr)
        print(f"   OR: python3 {sys.argv[0]} results [database_uri] <trait_name> <results_file>", file=sys.stderr)
        print(f"   OR: python3 {sys.argv[0]} results [database_uri] <trait_name> auto", file=sys.stderr)
        print(f"   OR: python3 {sys.argv[0]} results [database_uri] all", file=sys.stderr)
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
        if args == ['all']:
            import glob

            upload_curves_from_files(glob.glob(str(CURVE_PATH) + "/*/*.json"))
            upload_curves_from_files(glob.glob(str(CURVE_PATH_SIM) + "/*/*/*.json"))
        else:
            upload_curves_from_files(args)
    elif sys.argv[1] == "results":
        if args == ['all']:
            for trait_name in TRAIT_NAMES:
                results_file = Path(TRAIT_PATH, trait_name, str(trait_name) + ".json")
                upload_results_from_file(trait_name, results_file)
        else:
            trait_name = args[0]
            if args[1] == 'auto':
                results_file = Path(TRAIT_PATH, trait_name, str(trait_name) + ".json")
            else:
                results_file = args[1]
            upload_results_from_file(trait_name, results_file)
