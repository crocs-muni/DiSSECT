from typing import Dict, Any

import pandas as pd

import curve_analyzer.utils.database_handler as database
from curve_analyzer.definitions import STD_CURVE_DICT

db = None


def load_trait(trait: str, params: Dict[str, Any] = None, curve: str = None) -> pd.DataFrame:
    global db
    if not db:
        db = database.connect()

    return pd.DataFrame(database.get_trait_results(db, trait)).convert_dtypes()


def load_curves(filters: Any = {}) -> pd.DataFrame:
    global db
    if not db:
        db = database.connect()

    def project(record: Dict[str, Any]):
        projection = {}
        projection["curve"] = record["name"]
        projection["cofactor"] = int(record["cofactor"], base=16) if isinstance(record["cofactor"], str) else int(record["cofactor"])

        projection["bitlength"] = int(record["field"]["bits"])
        projection["simulated"] = record["simulated"]
        return projection

    df = pd.DataFrame(map(project, database.get_curves(db, filters, raw=True)))
    return df


def filter_df(df, choices):
    # TODO this way of checking is expensive - add curve categories to DB
    allowed_curves = []
    for source in choices["source"]:
        allowed_curves += STD_CURVE_DICT.get(source, [])

    if "sim" not in choices["source"]:
        df = df[df.simulated == False]

    if "std" not in choices["source"]:
        df = df[df.curve.isin(allowed_curves) | (df.simulated == True)]

    del choices["source"]

    for key, value in choices.items():
        options = list(map(int, value))
        df = df[df[key].isin(options)]

    return df
