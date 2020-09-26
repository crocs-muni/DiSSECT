#!/usr/bin/env sage

# A script for parallel running individual tests from the command line.

import argparse
import logging
import os

from curve_analyzer.definitions import TEST_PATH
from curve_analyzer.utils.parallel.job_manager.manager import ParallelRunner, Task, TaskResult

try:
    import coloredlogs

    coloredlogs.install(level=logging.INFO)
except Exception as e:
    print('E: Package coloredlogs is not installed. No logs will be displayed')

logger = logging.getLogger(__name__)


def load_test_parameters(args):
    jobs_total = args.jobs
    while args.jobs > 0:
        chunk = jobs_total - args.jobs + 1
        yield {'test_name': args.test_name, 'curve_type': args.curve_type, 'order_bound': args.order_bound,
               'description': "_part_" + str(chunk) + "_of_" + str(jobs_total), 'chunks_total': jobs_total,
               'chunk': chunk}
        args.jobs -= 1


def main():
    parser = argparse.ArgumentParser(description='Experiment parallelizer')
    parser.add_argument('-t', '--tasks', type=int, default=1,
                        help='Number of tasks to run in parallel (default: 1')
    parser.add_argument('-j', '--jobs', type=int, default=1,
                        help='Number of jobs to run in parallel (default: 1')
    parser.add_argument('-s', '--sage', default='sage',
                        help='Path to the sage')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-n', '--test_name', metavar='test_name', type=str, action='store',
                               help='the test identifier, e.g., a02', required=True)
    requiredNamed.add_argument('-c', '--curve_type', metavar='curve_type', type=str,
                               help='the type of curves to be tested; must be one of the following: std (all standard curves), sim (all simulated curves), sample (curves secp112r1, secp192r1, secp256r1), all (all curves in the database)',
                               required=True)
    parser.add_argument('-v', '--verbosity', action='store_true', help='verbosity flag (default: False)')
    parser.add_argument('-b', '--order_bound', action='store', type=int, metavar='order_bound', default=256,
                        help='upper bound for curve order bitsize (default: 256)')

    args = parser.parse_args()
    print(args)

    wrapper_path = os.path.join(TEST_PATH, 'run_tests_wrapper.py')

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
        for p in load_test_parameters(args):
            cli = ' '.join(['--%s=%s' % (k, p[k]) for k in p.keys()])
            if args.verbosity:
                cli = ' '.join([cli, '-v'])
            t = Task(args.sage, '%s %s' % (wrapper_path, cli))
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
        logger.info("Task %s finished, code: %s, fails: %s" % (r.job.idx, r.ret_code, r.job.failed_attempts))
        if r.ret_code != 0 and r.job.failed_attempts < 3:
            pr.enqueue(r.job)

    pr.job_feeder = feeder
    pr.cb_job_prerun = prerun
    pr.cb_job_finished = on_finished
    pr.work()


if __name__ == '__main__':
    main()
