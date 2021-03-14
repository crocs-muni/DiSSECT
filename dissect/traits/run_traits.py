#!/usr/bin/env python3

# A script for parallel running individual traits from the command line.

import argparse
import logging
import os

from dissect.definitions import TRAIT_PATH, TRAIT_NAMES
from dissect.utils.parallel.job_manager.manager import ParallelRunner, Task, TaskResult

try:
    import coloredlogs

    coloredlogs.install(level=logging.INFO)
except ModuleNotFoundError:
    print("E: Package coloredlogs is not installed. No logs will be displayed")

logger = logging.getLogger(__name__)


def load_trait_parameters(args):
    jobs_total = args.jobs
    while args.jobs > 0:
        chunk = jobs_total - args.jobs + 1
        yield {
            "trait_name": args.trait_name,
            "curve_type": args.curve_type,
            "order_bound": args.order_bound,
            "allowed_cofactors": args.allowed_cofactors,
            "description": "part_"
            + str(chunk).zfill(4)
            + "_of_"
            + str(jobs_total).zfill(4),
            "chunks_total": jobs_total,
            "chunk": chunk,
        }
        args.jobs -= 1


def main():
    parser = argparse.ArgumentParser(description="Experiment parallelizer")
    parser.add_argument(
        "-t",
        "--tasks",
        type=int,
        default=1,
        help="Number of tasks to run in parallel (default: 1",
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=1,
        help="Number of jobs to run in parallel (default: 1",
    )
    parser.add_argument("-s", "--sage", default="sage", help="Path to the sage")
    requiredNamed = parser.add_argument_group("required named arguments")
    requiredNamed.add_argument(
        "-n",
        "--trait_name",
        metavar="trait_name",
        type=str,
        action="store",
        help="the trait identifier; available traits: " + ", ".join(TRAIT_NAMES),
        required=True,
    )
    requiredNamed.add_argument(
        "-c",
        "--curve_type",
        metavar="curve_type",
        type=str,
        help="the type of curves for which to compute traits; must be one of the following: std (all standard "
        "curves), sim (all simulated curves), sample (curves secp112r1, secp192r1, "
        "secp256r1), all (all curves in the database)",
        required=True,
    )
    parser.add_argument(
        "-v", "--verbosity", action="store_true", help="verbosity flag (default: False)"
    )
    parser.add_argument(
        "-b",
        "--order_bound",
        action="store",
        type=int,
        metavar="order_bound",
        default=256,
        help="upper bound for curve order bitsize (default: 256)",
    )
    parser.add_argument(
        "-a",
        "--allowed_cofactors",
        nargs="+",
        metavar="allowed_cofactors",
        default=[1],
        help="the list of cofactors the curve can have (default: [1])",
    )

    args = parser.parse_args()
    if args.trait_name not in TRAIT_NAMES:
        print("please enter a valid trait identifier, e.g., a02")
        exit()
    print(args)

    wrapper_path = os.path.join(TRAIT_PATH, "run_traits_single.py")

    pr = ParallelRunner()
    pr.parallel_tasks = args.tasks

    def feeder():
        """
        Create function that generates computing jobs.
        ParallelRunner class takes any function that generates iterable of Task instances.
        Usually its best to implement it as a generator so jobs are generated on the fly and they don't
        have to be memorized. This function can be called several times during the computation
        to add new jobs to the computing queue.

        The general approach of using a function to generate Tasks gives us flexibility
        in terms of implementation. Here we use function that reads `args`, reads the input parameter
        file and generates tasks based on this information.
        The function also has an access to `pr` so it can adapt to job already being done.
        The function can also store its own state.
        """
        for p in load_trait_parameters(args):
            allowed_cofactors_string = " ".join(map(str, p["allowed_cofactors"]))
            del p["allowed_cofactors"]
            cli = " ".join(["--%s=%s" % (k, p[k]) for k in p.keys()])

            cli = " ".join([cli, "-a", allowed_cofactors_string])
            t = Task(args.sage, "%s %s" % (wrapper_path, cli))
            yield t

    def prerun(j: Task):
        """
        Function executed just after the Task is taken out from the queue and before
        executing by a worker.
        By setting j.skip = True this task will be skipped and not executed.
        You won't get notification about finishing
        """
        logger.info("Going to start task %s" % (j.idx,))

    def on_finished(r: TaskResult):
        """
        Called when task completes. Can be used to re-enqueue failed task.
        You also could open the result file and analyze it, but this could slow-down
        the job manager loop (callbacks are executed on manager thread).
        """
        logger.info(
            "Task %s finished, code: %s, fails: %s"
            % (r.job.idx, r.ret_code, r.job.failed_attempts)
        )
        if r.ret_code != 0 and r.job.failed_attempts < 3:
            pr.enqueue(r.job)

    pr.job_feeder = feeder
    pr.cb_job_prerun = prerun
    pr.cb_job_finished = on_finished
    pr.work()


if __name__ == "__main__":
    main()
