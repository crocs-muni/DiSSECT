from pathlib import Path
from typing import Dict, Any

import pandas as pd
from sage.all import ZZ, sage_eval

import curve_analyzer.utils.database_handler as database
from curve_analyzer.definitions import STD_CURVE_DICT, TRAIT_PATH
from curve_analyzer.utils.json_handler import load_from_json

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
        projection["cofactor"] = ZZ(record["cofactor"])
        projection["bitlength"] = ZZ(record["field"]["bits"])
        projection["simulated"] = record["simulated"]
        return projection

    df = pd.DataFrame(map(project, database.get_curves(db, filters, raw=True)))
    return df


def get_trait_params_dict(trait_name):
    params_file = load_from_json(Path(TRAIT_PATH, trait_name, trait_name + ".params"))
    params_names = params_file["params_local_names"]
    params_dict = {}
    for param_name in params_names:
        param_values = sage_eval(params_file["params_global"][param_name + "_range"])
        params_dict[param_name] = param_values
    params_dict_sorted = {key: params_dict[key] for key in sorted(params_dict)}
    return params_dict_sorted


def filter_df_by_trait_params(df, trait_name, allowed_trait_params_list):
    params_dict = get_trait_params_dict(trait_name)
    assert len(params_dict.keys()) == len(allowed_trait_params_list)
    for (i, param_name) in enumerate(params_dict.keys()):
        df = df[df[param_name].isin(allowed_trait_params_list[i])]
    return df


def filter_df(df, sources, bitlengths, cofactors, trait_name=None, allowed_trait_params_list=None):
    bitlengths = map(ZZ, bitlengths)
    cofactors = map(ZZ, cofactors)
    allowed_curves = []
    for source in sources:
        try:
            allowed_curves += STD_CURVE_DICT[source]
        except KeyError:
            pass
    if "sim" in sources:
        if "std" not in sources:
            df = df[df.curve.isin(allowed_curves) | (df.simulated == True)]
    elif "std" in sources:
        df = df[df.simulated == False]
    else:
        df = df[df.curve.isin(allowed_curves) & (df.simulated == False)]
    df = df[df.bitlength.isin(bitlengths)]
    df = df[df.cofactor.isin(cofactors)]
    if trait_name and allowed_trait_params_list:
        df = filter_df_by_trait_params(df, trait_name, allowed_trait_params_list)
    return df
