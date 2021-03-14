import json

from sage.all import Integer

FLOAT_PRECISION = 5


class IntegerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Integer):
            return int(obj)
        if isinstance(obj, float):
            return round(obj, 5)
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)


def save_into_json(results, fname, mode="a", indent=2):
    with open(fname, mode) as f:
        json.dump(results, f, indent=indent, cls=IntegerEncoder)


def load_from_json(fname):
    with open(fname, "r") as f:
        results = json.load(f)
    return results
