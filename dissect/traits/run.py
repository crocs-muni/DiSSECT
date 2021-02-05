#!/usr/bin/env sage

import argparse
import sys
import os
import pathlib
import itertools
import json
from multiprocessing import Process, Queue, Lock
from sage.all import sage_eval

from dissect.definitions import TRAIT_NAMES, TRAIT_PATH, TRAIT_MODULE_PATH
from dissect.utils.database_handler import connect, store_trait_result, is_solved, get_curves, create_trait_index


def params_range(trait_name):
    with open(pathlib.Path(TRAIT_PATH, trait_name, trait_name + '.params'), "r") as params_file:
        params = json.load(params_file)

    params_names = params["params_local_names"]
    params_ranges = {}
    for key in params["params_global"].keys():
        params_ranges[key] = sage_eval(params["params_global"][key])

    for params_values in itertools.product(*params_ranges.values()):
        # TODO this IMO is not guaranteed to work -> relies on ordering of hashmap
        yield dict(zip(params_names, params_values))


def get_trait_function(trait):
    module_name = TRAIT_MODULE_PATH + "." + trait + '.' + trait
    try:
        __import__(module_name)
    except ModuleNotFoundError:
        return None
    return getattr(sys.modules[module_name], trait + "_curve_function")


def producer(database, trait, args, queue, lock):
    db = connect(database)
    create_trait_index(db, trait)

    with lock:
        print("Producer starting ...")

    curves = get_curves(db, filters=args)
    for curve in curves:
        for params in params_range(trait):
            # TODO check if curve is not mutated ~ if it can be safely passed into the queue
            queue.put((curve, params), block=True)

    with lock:
        print("Done - producer shutting down ...")

    for _ in range(args.jobs):
        queue.put((None, None))


def consumer(identifier, database, trait, queue, lock):
    db = connect(database)
    trait_function = get_trait_function(trait)
    if not trait_function:
        with lock:
            print(f"Consumer {identifier:2d} could not be initialized")
        return

    with lock:
        print(f"Consumer {identifier:2d} started")

    while True:
        curve, params = queue.get()
        if curve is params is None:
            with lock:
                print(f"Consumer {identifier:2d} stopped")
            return
        if is_solved(db, curve, trait, params):
            continue
        trait_result = trait_function(curve, **params)
        store_trait_result(db, curve, trait, params, trait_result)


def main():
    parser = argparse.ArgumentParser(
        description='Welcome to Curve analyzer! It allows you to run traits on a selected subset of standard or '
                    'simulated curves.')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-n', '--trait_name', metavar='trait_name', type=str, action='store',
                               help='the trait identifier; available traits: ' + ", ".join(TRAIT_NAMES), required=True)
    requiredNamed.add_argument('-c', '--curve_type', metavar='curve_type', type=str, choices=["std", "sim", "sample", "all"],
                               help='the type of curves or which to compute traits; must be one of the following: std (all standard '
                                    'curves), sim (all simulated curves), sample (curves secp112r1, secp192r1, '
                                    'secp256r1), all (all curves in the database)',
                               required=True)
    parser.add_argument('-b', '--order_bound', action='store', type=int, metavar='order_bound', default=256,
                        help='upper bound for curve order bitsize (default: 256)')
    parser.add_argument('-a', '--allowed_cofactors', nargs='+', metavar='allowed_cofactors', default=None,
                        help='the list of cofactors the curve can have (default: all)')
    parser.add_argument('-j', '--jobs', metavar='jobs', type=int, default=1,
                        help='Number of jobs to run in parallel (default: 1)')
    parser.add_argument('--database', metavar='database', type=str, default="mongodb://localhost:27017/",
                        help='Database URI (default: mongodb://localhost:27017/)')

    args = parser.parse_args()

    queue = Queue(1000)
    lock = Lock()

    consumers = [Process(target=consumer, args=(i, args.database, args.trait_name, queue, lock)) for i in range(1, args.jobs + 1)]
    for proc in consumers:
        proc.daemon = True
        proc.start()

    producer(args.database, args.trait_name, args, queue, lock)

    for proc in consumers:
        proc.join()


if __name__ == '__main__':
    main()
