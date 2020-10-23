#!/usr/bin/env sage
import os, json, itertools,sys
from sage.all import sage_eval
from curve_analyzer.utils.json_handler import *
from curve_analyzer.utils.custom_curve import CustomCurve
from curve_analyzer.definitions import TEST_PATH, TEST_MODULE_PATH, TEST_prefixes


tests_to_skip = ['a08']

curve = CustomCurve({
      "name": "brainpoolP160r1",
      "category": "brainpool",
      "desc": "",
      "oid": "1.3.36.3.3.2.8.1.1.1",
      "field": {
        "type": "Prime",
        "p": "0xe95e4a5f737059dc60dfc7ad95b3d8139515620f",
        "bits": 160
      },
      "form": "Weierstrass",
      "params": {
        "a": {
          "raw": "0x340e7be2a280eb74e2be61bada745d97e8f7c300"
        },
        "b": {
          "raw": "0x1e589a8595423412134faa2dbdec95c8d8675e58"
        }
      },
      "generator": {
        "x": {
          "raw": "0xbed5af16ea3f6a4f62938c4631eb5af7bdbcdbc3"
        },
        "y": {
          "raw": "0x1667cb477a1a8ec338f94741669c976316da6321"
        }
      },
      "order": "0xe95e4a5f737059dc60df5991d45029409e60fc09",
      "cofactor": "0x1",
      "characteristics": {
        "discriminant": "845365293605815390445478703156256339281515926196",
        "j_invariant": "387367055434500543477184371239969891945180101787",
        "trace_of_frobenius": "519972310379544251229703",
        "embedding_degree": "444099199480014958275695012943393788070980856152",
        "anomalous": False,
        "supersingular": False,
        "cm_disc": "592132265973353277700926857248628510609391551437",
        "conductor": "3",
        "torsion_degrees": [
          {
            "r": 2,
            "least": 3,
            "full": 3
          },
          {
            "r": 3,
            "least": 2,
            "full": 6
          },
          {
            "r": 5,
            "least": 12,
            "full": 12
          },
          {
            "r": 7,
            "least": 8,
            "full": 8
          },
          {
            "r": 11,
            "least": 5,
            "full": 55
          }
        ]
      }
    })

def compute_results(test_name):
    module_name = TEST_MODULE_PATH+'.'+test_name + '.' + test_name
    __import__(module_name)
    curve_function = getattr(sys.modules[module_name], test_name+"_curve_function")
    main_json_file = os.path.join(TEST_PATH, test_name, test_name +'_structure'+ '.json')
    params_file = os.path.join(TEST_PATH, test_name, test_name + '.params')
    results= {curve.name:{}}
    with open(params_file, 'r') as f:
        params = json.load(f)
    for key in params["params_global"].keys():
        params["params_global"][key] = sage_eval(params["params_global"][key])
    params_global = params["params_global"]
    params_local_names = params["params_local_names"]
    params_local_values = list(itertools.product(*params_global.values()))[0]
    params_local = dict(zip(params_local_names, params_local_values))
    results[curve.name][str(params_local)] = curve_function(curve, *params_local_values)
    save_into_json(results,main_json_file,mode = 'w')



def main():
    directory = TEST_PATH
    for filename in os.listdir(directory):
        if filename in tests_to_skip:
            continue
        if not filename[0] in TEST_prefixes:
            continue
        try:
            int(filename[1:],10)
        except:
            continue
        compute_results(filename)

main()





