#!/usr/bin/env python3

import argparse
import itertools
import json
import pathlib
import sys
import datetime
from math import prod
from multiprocessing import Process, Queue, Lock

from sage.all import sage_eval
from pymongo.errors import ServerSelectionTimeoutError

from dissect.definitions import TRAIT_NAMES, TRAIT_PATH, TRAIT_MODULE_PATH
from dissect.utils.database_handler import (
    connect,
    store_trait_result,
    is_solved,
    get_curves,
    get_curves_count,
    get_trait_results_count,
    create_trait_index,
)
import dissect.traits.trait_info as trait_info
from dissect.utils.custom_curve import CustomCurve


def get_trait_function(trait):
    module_name = TRAIT_MODULE_PATH + "." + trait + "." + trait
    try:
        __import__(module_name)
    except ModuleNotFoundError:
        return None
    return getattr(sys.modules[module_name], trait + "_curve_function")


def tprint(string):
    print(f"[{datetime.datetime.now()}] {string}")


def producer(database, trait, args, queue, lock):
    db = connect(database)
    create_trait_index(db, trait)

    with lock:
        tprint("Preliminary check")

    total = get_curves_count(db, query=vars(args)) * prod(map(len, trait_info.params(trait).values()))
    computed = get_trait_results_count(db, trait, query=vars(args))

    with lock:
        print(f"Computed {computed}/{total}")
        tprint("Producer start")

    curves = map(CustomCurve, get_curves(db, query=vars(args)))
    counter = 0
    iterator = itertools.product(curves, trait_info.params_iter(trait))
    while counter <= args.skip:
        next(iterator)
        counter += 1

    for curve, params in iterator:
        queue.put((curve, params), block=True)
        if args.verbose:
            print(f"{counter:>9} {curve.name()}:{params}")
        counter += 1

    for _ in range(args.jobs):
        queue.put((None, None))

    with lock:
        tprint("Producer finish")


def consumer(identifier, database, trait, queue, lock):
    db = connect(database)
    trait_function = get_trait_function(trait)
    if not trait_function:
        with lock:
            tprint(f"Consumer {identifier:2d} could not be initialized")
        return

    with lock:
        tprint(f"Consumer {identifier:2d} started")

    while True:
        curve, params = queue.get()
        if curve is params is None:
            with lock:
                tprint(f"Consumer {identifier:2d} stopped")
            return

        for i in range(3): # TODO move to db_handler?
            try:
                solved = is_solved(db, curve, trait, params)
                break
            except ServerSelectionTimeoutError:
                tprint(f"Server timeout: Reconnection attempt {i}")
                db = connect(database)

        if solved:
            continue

        trait_result = trait_function(curve, **params)
        if not trait_result:
            continue

        for i in range(3):
            try:
                store_trait_result(db, curve, trait, params, trait_result)
                break
            except ServerSelectionTimeoutError:
                tprint(f"Server timeout: Reconnection attempt {i}")
                db = connect(database)



def main():
    parser = argparse.ArgumentParser(
        description="Welcome to DiSSECT! It allows you to run traits on a selected subset of standard or simulated curves."
    )
    parser.add_argument(
        "-n",
        "--trait_name",
        metavar="trait_name",
        help="Trait identifier",
        required=True
    )
    parser.add_argument(
        "-c",
        "--category",
        nargs="+",
        help="Curve category",
        default=["all"]
    )
    parser.add_argument(
        "-b",
        "--bits",
        nargs="+",
        default=["all"],
        help="Curve bitlength",
    )
    parser.add_argument(
        "--cofactor",
        nargs="+",
        default=["all"],
        help="Curve cofactor",
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=1,
        help="Number of jobs to run in parallel (default: 1)",
    )
    parser.add_argument(
        "--database",
        default="mongodb://localhost:27017/",
        help="Database URI (default: mongodb://localhost:27017/)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--skip",
        type=int,
        default=0,
        help="Skip given number of curve-parameter combinations"
    )

    args = parser.parse_args()

    queue = Queue(1000)
    lock = Lock()

    with lock:
        tprint("Script start")

    consumers = [
        Process(target=consumer, args=(i, args.database, args.trait_name, queue, lock))
        for i in range(1, args.jobs + 1)
    ]
    for proc in consumers:
        proc.daemon = True
        proc.start()

    producer(args.database, args.trait_name, args, queue, lock)

    for proc in consumers:
        proc.join()

    with lock:
        tprint("Script finish")


if __name__ == "__main__":
    main()
