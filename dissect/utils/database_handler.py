#!/usr/bin/env python3
import bz2
import json
import os
from typing import Optional, Tuple, Iterable, Dict, Any

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from dissect.traits import TRAITS


def connect(database: Optional[str] = None) -> Database:
    client = MongoClient(database, connect=False)
    return client["dissect"]


def create_curves_index(db: Database) -> None:
    db["curves"].create_index([("name", 1)], unique=True)


def create_trait_index(db: Database, trait: str) -> None:
    db[f"trait_{trait}"].create_index([("curve.name", 1), ("params", 1)], unique=True)


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
            curve["generator"]["y"]["raw"] or curve["generator"]["y"]["poly"]
        ):
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

    c["standard"] = curve.get("standard", False if "sim" in curve["category"] else True)
    c["example"] = curve.get("example", False)

    if curve.get("simulation"):
        sim = curve["simulation"]
    else:
        sim = {}
        if "seed" in curve and curve["seed"]:
            sim["seed"] = hex(int(curve["seed"], base=16))
        elif (
            "characteristics" in curve
            and "seed" in curve["characteristics"]
            and curve["characteristics"]["seed"]
        ):
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


def import_curves(db: Database, curves: json) -> Tuple[int, int]:
    try:
        if not isinstance(
            curves, list
        ):  # inconsistency between simulated and standard format
            curves = curves["curves"]
    except Exception:  # invalid format
        return 0, 0

    create_curves_index(db)

    success = 0
    for curve in curves:
        try:
            if db["curves"].insert_one(_format_curve(curve)):
                success += 1
        except DuplicateKeyError:
            pass

    return success, len(curves)


def import_trait_results(
    db: Database, trait_name: str, trait_results: json = None
) -> Tuple[int, int]:
    create_trait_index(db, trait_name)

    success = 0
    total = 0
    for result in trait_results:
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


def get_curves(db: Database, query: Any = None) -> Iterable[Any]:
    aggregate_pipeline = []
    aggregate_pipeline.append(
        {"$match": format_curve_query(query) if query else dict()}
    )
    aggregate_pipeline.append({"$unset": "_id"})
    curves = list(db["curves"].aggregate(aggregate_pipeline))

    return map(_decode_ints, curves)


def get_curves_count(db: Database, query: Any = None) -> int:
    return db["curves"].count_documents(format_curve_query(query) if query else dict())


def get_curve_categories(db: Database) -> Iterable[str]:
    return db["curves"].distinct("category")


def format_curve_query(query: Dict[str, Any]) -> Dict[str, Any]:
    result = {}

    def helper(key, cast, db_key=None):
        if key not in query:
            return

        db_key = db_key if db_key else key

        if isinstance(query[key], list):
            if len(query[key]) == 0 or "all" in query[key]:
                return
            if len(query[key]) == 1:
                result[db_key] = cast(query[key][0])
            else:
                result[db_key] = {"$in": list(map(cast, query[key]))}
        elif query[key] != "all":
            result[db_key] = cast(query[key])

    helper("name", str)
    helper("standard", lambda x: str(x).lower() == "true")
    helper("example", lambda x: str(x).lower() == "true")
    helper("category", str)
    helper("bits", int, "field.bits")
    helper("cofactor", lambda x: hex(int(x)))
    helper("field_type", str, "field.type")

    return result


def _cast_sage_types(result: Any) -> Any:
    from sage.all import Integer

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
    from sage.all import Integer

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
    curve: Any,
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
    trait_result["curve"]["field_type"] = curve.field_type()
    trait_result["curve"]["cofactor"] = hex(curve.cofactor())
    trait_result["curve"] = _cast_sage_types(trait_result["curve"])
    trait_result["params"] = _cast_sage_types(params)
    trait_result["result"] = _encode_ints(result)
    try:
        return db[f"trait_{trait}"].insert_one(trait_result).acknowledged
    except DuplicateKeyError:
        return False


def is_solved(db: Database, curve: Any, trait: str, params: Dict[str, Any]) -> bool:
    trait_result = {"curve.name": curve.name()}
    trait_result["params"] = _cast_sage_types(params)
    return db[f"trait_{trait}"].find_one(trait_result) is not None


def get_trait_results(
    db: Database, trait: str, query: Dict[str, Any] = None, limit: int = None
):
    aggregate_pipeline = []
    aggregate_pipeline.append(
        {"$match": format_trait_query(trait, query) if query else dict()}
    )
    aggregate_pipeline.append({"$unset": "_id"})
    if limit:
        aggregate_pipeline.append({"$limit": limit})

    aggregated = list(db[f"trait_{trait}"].aggregate(aggregate_pipeline))
    return map(_decode_ints, map(_flatten_trait_result, aggregated))


def get_trait_results_count(db: Database, trait: str, query: Dict[str, Any] = None):
    return db[f"trait_{trait}"].count_documents(
        format_trait_query(trait, query) if query else dict()
    )


def format_trait_query(trait_name: str, query: Dict[str, Any]) -> Dict[str, Any]:
    result = {}
    query = query.copy()

    def helper(key, cast, db_key=None):
        if key not in query:
            return

        db_key = db_key if db_key else key

        if isinstance(query[key], list):
            if len(query[key]) == 0 or "all" in query[key]:
                return
            if len(query[key]) == 1:
                result[db_key] = cast(query[key][0])
            else:
                result[db_key] = {"$in": list(map(cast, query[key]))}
        elif query[key] != "all":
            result[db_key] = cast(query[key])

        del query[key]

    helper("name", str, "curve.name")
    helper("standard", lambda x: str(x).lower() == "true", "curve.standard")
    helper("example", lambda x: str(x).lower() == "true", "curve.example")
    helper("category", str, "curve.category")
    helper("bits", int, "curve.bits")
    helper("cofactor", lambda x: hex(int(x)), "curve.cofactor")
    helper("field_type", str, "curve.field_type")

    for key in TRAITS[trait_name].INPUT:
        helper(key, TRAITS[trait_name].INPUT[key][0], f"params.{key}")

    for key in TRAITS[trait_name].OUTPUT:
        helper(
            key,
            lambda x: _encode_ints(TRAITS[trait_name].OUTPUT[key][0](x)),
            f"result.{key}",
        )

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
    if isinstance(source, str) and (
        source[:2].lower() == "0x" or source[:3].lower() == "-0x"
    ):
        return int(source, base=16)
    if isinstance(source, dict):
        for key, value in source.items():
            source[key] = _decode_ints(value)
    elif isinstance(source, list):
        for idx, value in enumerate(source):
            source[idx] = _decode_ints(value)
    return source


def import_file(db: Database, path: str):
    name = os.path.basename(path)
    if name.startswith("trait_"):
        trait_name = name[len("trait_") :].split(os.extsep, 1)[0]
        print(f"Importing trait {trait_name} from {name}")
        if name.endswith(".json.bz2"):
            with bz2.open(path, "rb") as f:
                results = json.load(f)
        elif name.endswith(".json"):
            with open(path, "r") as f:
                results = json.load(f)
        else:
            raise ValueError("Invalid file format")

        succ, total = import_trait_results(db, trait_name, results)
        print(f"- imported {succ} out of {total} trait results")
    else:
        print(f"Importing curves from {name}")

        if name.endswith(".json"):
            with open(path, "r") as f:
                curves = json.load(f)
        elif name.endswith(".json.bz2"):
            with bz2.open(path, "rb") as f:
                curves = json.load(f)
        else:
            raise ValueError("Invalid file format")

        succ, total = import_curves(db, curves)
        print(f"- imported {succ} out of {total} curves")


def main():
    import argparse
    import tempfile
    import tarfile
    import shutil

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--database_url", type=str, default="mongodb://localhost:27017/"
    )
    subparsers = parser.add_subparsers(dest="command")

    parser_export = subparsers.add_parser("export")
    parser_export.add_argument("-o", "--output", type=str, default="dissect.tar")
    parser_export.add_argument("--no-curves", default=False, action="store_true")
    parser_export.add_argument("--no-traits", default=False, action="store_true")
    parser_export.add_argument("--trait", type=str, default=["all"], nargs="*")

    parser_import = subparsers.add_parser("import")
    parser_import.add_argument("-i", "--input", type=str, default="dissect.tar")

    args = parser.parse_args()

    db = connect(args.database_url)

    with tempfile.TemporaryDirectory() as tmpdir:

        def export_records(collection_name):
            document_count = db[collection_name].estimated_document_count()

            if document_count == 0:
                print(f"Skipping {collection_name} (no records)")
                return

            with open(os.path.join(tmpdir, f"{collection_name}.json.bz2"), "wb") as f:
                print(f"Exporting {collection_name} (~{document_count} records)")
                compressor = bz2.BZ2Compressor()
                f.write(compressor.compress(b"[\n"))
                for idx, record in enumerate(db[collection_name].find()):
                    if idx != 0:
                        f.write(compressor.compress(b",\n"))
                    del record["_id"]
                    f.write(compressor.compress(json.dumps(record, indent=2).encode()))
                f.write(compressor.compress(b"\n]\n"))
                f.write(compressor.flush())

        if args.command == "export":
            if not args.no_curves:
                export_records("curves")

            if not args.no_traits:
                trait_collections = list(
                    filter(lambda x: x.startswith("trait_"), db.list_collection_names())
                )
                if not "all" in args.trait:
                    trait_collections = list(
                        filter(
                            lambda x: x[len("trait_") :] in args.trait,
                            trait_collections,
                        )
                    )
                for trait_collection in trait_collections:
                    export_records(trait_collection)

            output_files = os.listdir(tmpdir)

            if os.path.isdir(args.output):
                for file in output_files:
                    shutil.copyfile(
                        os.path.join(tmpdir, file), os.path.join(args.output, file)
                    )
            elif len(output_files) == 1 and args.output.endswith(".json.bz2"):
                shutil.copyfile(
                    os.path.join(tmpdir, output_files[0]),
                    args.output,
                )
            elif len(output_files) == 1 and args.output.endswith(".json"):
                with open(args.output, "wb") as output_file, open(
                    os.path.join(tmpdir, output_files[0]), "rb"
                ) as input_file:
                    decompressor = bz2.BZ2Decompressor()
                    for data in iter(lambda: input_file.read(1024 * 1024), b""):
                        output_file.write(decompressor.decompress(data))
            else:
                with tarfile.open(args.output, "w") as tar:
                    for file in output_files:
                        tar.add(f"{tmpdir}/{file}", arcname=file)

        elif args.command == "import":
            if args.input.endswith(".tar"):
                with tempfile.TemporaryDirectory() as tmpdir:
                    with tarfile.open(args.input, "r") as tar:
                        tar.extractall(tmpdir)

                    files = set(os.listdir(tmpdir))
                    trait_files = set(
                        filter(
                            lambda x: os.path.basename(x).startswith("trait_"),
                            files,
                        )
                    )
                    curve_files = files - trait_files
                    for file in list(curve_files) + list(trait_files):
                        import_file(db, os.path.join(tmpdir, file))
            elif args.input.endswith(".json") or args.input.endswith(".json.bz2"):
                import_file(db, args.input)
            else:
                print("Unknown input format")


if __name__ == "__main__":
    main()
