import json

from sage.all import *  # import sage library


# from sage.all import polynomial_modn_dense_ntl


class IntegerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, sage.rings.integer.Integer):
            return int(obj)

        # if isinstance(obj, polynomial_modn_dense_ntl.Polynomial_dense_mod_p):
        #    return str(obj)
        try:
            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, obj)
        except:
            return str(obj)


def save_into_json(results, fname, mode='a', indent=2):
    with open(fname, mode) as f:
        json.dump(results, f, indent=indent, cls=IntegerEncoder)


def load_from_json(fname):
    with open(fname, 'r') as f:
        results = json.load(f)
    return results
