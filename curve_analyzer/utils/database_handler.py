from pymongo import MongoClient
from curve_analyzer.utils.custom_curve import CustomCurve
from sage.all import Integer


def create_trait_index(db, trait):
    db[f"trait_{trait}"].create_index([("curve", 1), ("params", 1)], unique=True)


def connect(database=None):
    client = MongoClient(database)
    return client["dissect"]


def get_curves(db, filters):
    curve_filter = {}

    # Curve type filter
    if filters.curve_type == "sim":
        curve_filter["category"] = 1
    elif filters.curve_type == "std":
        curve_filter["category"] = 2

    # Bit-length filter
    curve_filter["field.bits"] = { "$lte": filters.order_bound }

    # Cofactor filter
    # TODO discuss if (allowed_cofactor == None => match_any) is ok
    if filters.allowed_cofactors:
        curve_filter["cofactor"] = { "$in": list(map(int, filters.allowed_cofactors)) }

    return map(CustomCurve, db.curves.find(curve_filter))


# TODO this should be IMO handled by the traits - after finishing computation transform Sage values into Python values
def _cast_sage_types(result):
    if isinstance(result, Integer):
        return int(result)
    elif isinstance(result, dict):
        for key, value in result.items():
            result[key] = _cast_sage_types(value)
    return result


def store_trait_result(db, curve, trait, params, result):
    trait_result = { "curve": curve.name }
    trait_result["params"] = _cast_sage_types(params)
    trait_result["result"] = _cast_sage_types(result)
    db[f"trait_{trait}"].insert_one(trait_result)


def is_solved(db, curve, trait, params):
    trait_result = { "curve": curve.name }
    trait_result["params"] = _cast_sage_types(params)
    return db[f"trait_{trait}"].find_one(trait_result) is not None

# TODO curve upload
