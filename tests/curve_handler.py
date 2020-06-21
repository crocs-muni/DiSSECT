from sage.all_cmdline import *   # import sage library

# importing nbs:
# https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html

import json
import os
import time
import sys
import fnmatch
import hashlib
import re
from prettytable import PrettyTable
# http://zetcode.com/python/prettytable/

CURVE_PATH = '../curves_json'
FILTER_PATH = '../filters/ord_to_name.json'

def import_curve_db(root = CURVE_PATH):
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
                suffix = "-" + str(re.findall(r'\d+', file)[0 ])
            with open(os.path.join(path, file)) as f:
                curve_db[source + suffix] = json.load(f)
    return curve_db

# sources = ['anssi', 'bls', 'bn', 'brainpool', 'gost', 'mnt', 'nist', 'other', 'secg', 'x962']
#114 curves in total, 83 unique orders

def count_curves(curve_db):
    total = 0 
    sources = curve_db.keys()
    for source in sources:
        count = len(curve_db[source]['curves'])
        total += count
        print(source, count)
    return total

def filter_out_sources(curve_db, filtering_source_list, filtering_curve_list):
    filtered_curve_db = {}
    sources = curve_db.keys()
    for source in sources:
        if not any(word in source for word in filtering_source_list):
            filtered_curve_db[source] = curve_db[source]
    return filtered_curve_db

def get_exact_duplicities(curve_db, verbose = False):
    sources = curve_db.keys()
    duplicities = []
    for source in sources:
        for curve in curve_db[source]['curves']:
            try:
                aliases = curve['aliases']
                name = source + '/' + curve['name']
                if verbose:
                    print(name + ": ", aliases)
                if not name in duplicities:
                    for string in aliases:
                        if not string in duplicities:
                            duplicities.append(string)
            except:
                continue
    return duplicities
            
def get_orders(curve_db):
    orders = []
    sources = curve_db.keys()
    for source in sources:
         for curve in curve_db[source]['curves']:
                order = ZZ(curve['order'])
                orders.append(order)
    return orders

def curve_gen(curve_db):
    sources = curve_db.keys()
    for source in sources:
        curves = curve_db[source]['curves']
        for curve in curves:
            yield curve

def write_list_to_file(l, fname = "test.txt"):
    with open(fname, 'w') as f:
        f.write(str(l))

class IntegerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Integer):
            return int(obj)

         # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
        
def save_into_json(results, fname, mode = 'a'):
    with open(fname, mode) as f:
        json.dump(results, f, indent = 2 , cls = IntegerEncoder)
        
def load_from_json(fname):
    with open(fname, 'r') as f:
        results = json.load(f)
    return results

def bitlen_sorted_names_gen():
    l = load_from_json(FILTER_PATH)
    sorted_orders = sorted(l.keys(), key = lambda x: ZZ(x))
    sorted_names = [l[o] for o in sorted_orders]
    for name in sorted_names:
        yield name

def montgomery_to_short_weierstrass(F, A, B, x, y):
    a = F( (3 -A**2 )/(3 *B**2 ) )
    b = F( (2 *A**3  - 9 *A)/(27 *B**3 ) )
    u = F( (3 *x+A)/(3 *B) )
    v = F( y/B )
    assert (u, v) in EllipticCurve(F, [a,b])
    return (a, b, u, v)

def twisted_edwards_to_montgomery(F, a, d, u, v, scaling = True):
    A = F( (2 *a + 2 *d)/(a- d) )
    B = F( 4 /(a - d) )
    if not B.is_square():
        scaling = False
    s = F(1 /B).sqrt()
    x = F( (1  + v)/(1  - v) )
    y = F( (1  + v)/((1  - v) * u) )
    if scaling:
        assert (x, y/s) in EllipticCurve(F, [0 , A, 0 , 1 , 0 ])
        return (A, 1 , x, y/s)
    return (A, B, x, y)

def twisted_edwards_to_short_weierstrass(F, aa, d, x, y, composition = False):
    if composition:
        A, B, x, y = twisted_edwards_to_montgomery(F, a, d, u, v, True)
        a, b, u, v = montgomery_to_short_weierstrass(F, A, B, x, y)
    else:
        a = F((aa**2  + 14  * aa * d + d**2 ) )/F(-48)
        b = F((aa+d) * (-aa**2  + 34  * aa * d - d**2 ) )/F(864 )
        u = (5 *aa + aa*y - 5 *d*y - d)/(12  - 12 *y)
        v = (aa + aa*y - d*y -d)/(4 *x - 4 *x*y)
    assert (u, v) in EllipticCurve(F, [a,b])
    return (a, b, u, v)

class CustomCurve:
    
    def __init__(self, db_curve):
        '''the "fixed" part of attributes'''
        self.name = db_curve['name']
        self.order = ZZ(db_curve['order'])
        self.source = db_curve['category']
        self.field = db_curve['field']
        self.form = db_curve['form']
        self.params = db_curve['params']
        self.desc = db_curve['desc']
        self.cofactor = ZZ(db_curve['cofactor'])
        self.nbits =  self.order.nbits()
        self.EC = None
        self.generator = None
        self.q = None
        self.trace = None
        '''the "variable" part of attributes'''    
        try:
            self.seed = db_curve['seed']
        except KeyError:
            self.seed = None
        try:
            self.x = ZZ(db_curve['generator']['x'])
            self.y = ZZ(db_curve['generator']['y'])
        except TypeError:
            self.x = None
            self.y = None
    #         self.characteristics = db_curve['characteristics']
        self.set()

    def set_generator(self, coord1, coord2, binary = False):
        if self.x == None or self.y == None:
            self.generator = None
        else:
            if binary:
                self.generator = self.EC(K.fetch_int(coord1), K.fetch_int(coord2))
            else:
                self.generator = self.EC(coord1, coord2)

    def set(self):
        x = self.x
        y = self.y
        if self.form == "Weierstrass":
            a = ZZ(self.params['a'])
            b = ZZ(self.params['b'])
            if self.field['type'] == "Prime":
                p = ZZ(self.field['p'])
                self.EC = EllipticCurve(GF(p), [a,b])
                self.set_generator(x,y)
            elif self.field['type'] == "Binary":
                exponents = list(self.field['poly'].values())
                exponents.append(0 )
                F = GF(2 )['w']; (w,) = F._first_ngens(1)
                modulus = 0 
                for e in exponents:
                    modulus += w**e
                m = ZZ(self.field['poly']['m'])
                K = GF(2 **m, 'w', modulus)
                self.EC = EllipticCurve(K, [1 ,K.fetch_int(ZZ(a)),0 ,0 ,K.fetch_int(ZZ(b))]) #xy, x^2, y, x, 1
                # print(self.EC)
                self.generator = None
                # self.set_generator(x,y)
                # needs fixing, originally:
                # self.generator = self.EC(K.fetch_int(x), K.fetch_int(y))

        elif self.form == "Montgomery":
            A = ZZ(self.params['a'])
            B = ZZ(self.params['b'])
            p = ZZ(self.field['p'])
            F = GF(p)
            a, b, u, v = montgomery_to_short_weierstrass(F, A, B, x, y)
            self.EC = EllipticCurve(F, [a,b])
            self.set_generator(u,v)

        elif self.form in ["Edwards", "TwistedEdwards"]:
            #we assume c=1
            if self.form == "Edwards":
                aa = 1 
            if self.form == "TwistedEdwards":
                aa = ZZ(self.params['a'])
            d = ZZ(self.params['d'])
            p = ZZ(self.field['p'])
            F = GF(p)
            a, b, xx, yy = twisted_edwards_to_short_weierstrass(F, aa, d, x, y)
            self.EC = EllipticCurve(F, [a,b])
            self.set_generator(xx,yy)
        else:
            self.EC = "Not implemented"

        self.q = self.EC.base_field().order()
        self.trace = self.q + 1  - self.order * self.cofactor

    def __repr__(self):
        return self.name + ": " + str(self.nbits) + "-bit curve in " + self.form + " form over " + self.field['type'] + " field" 
    
    def __str__(self):
        return self.name + ": " + str(self.nbits) + "-bit curve in " + self.form + " form over " + self.field['type'] + " field" 

    def __lt__(self, other):
        return (self.order, self.name) < (other.order, other.name)

class SimulatedWeierstrassCurve():
    def __init__(self, F, a, b, seed):
        self.F = F
        self.nbits = self.F.order().nbits()
        self.a = F(a)
        self.b = F(b)
        self.seed = seed
        self.EC = EllipticCurve(F, [a, b])
        self.order = self.EC.order()

    def __repr__(self):
        return str(self.nbits) + "-bit Weierstrass curve"
    
    def __str__(self):
        return str(self.nbits) + "-bit Weierstrass curve"

    def __lt__(self, other):
        return (self.order) < (other.order)

# print(vars(curve))

def custom_curve_gen(curve_db):
    for db_curve in curve_gen(curve_db):
        curve = CustomCurve(db_curve)
        yield curve

def custom_curves(curve_db):
    return [c for c in custom_curve_gen(curve_db)]

def custom_curves_sorted_by_name(curve_db):
    return sorted(custom_curves(curve_db), key = lambda item: item.name)

def bitlen_sorted_custom_curve_gen():
    l = load_from_json('/home/x408178/Research/Curve_checker/filters/ord_to_name.json')
    sorted_orders = sorted(l.keys(), key = lambda x: ZZ(x))
    sorted_names = [l[o] for o in sorted_orders]
    for name in sorted_names:
        yield name

def embedding_degree_q(q, r):
    '''returns embedding degree with respect to q'''
    return Mod(q,r).multiplicative_order()

def embedding_degree(E, r):
    '''returns relative embedding degree with respect to E'''
    q = (E.base_field()).order()
    return embedding_degree_q(q, r)

try:
    curve_db
except NameError:
    curve_db = import_curve_db(CURVE_PATH)

try:
    curves
except NameError:
    curves = sorted(custom_curves(curve_db))

try:
    curves_sample
except NameError:
    curves_sample = [c for c in curves if c.name in ["secp112r1", "secp192r1", "secp256r1"]]

try:
    curves_sim
except NameError:
    curves_sim = [c for c in curves if "sim" in c.name]

try:
    curves_std
except NameError:
    curves_std = [c for c in curves if not "sim" in c.name]

