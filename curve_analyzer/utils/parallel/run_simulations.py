import json
import os
import argparse
import logging
from job_manager.manager import ParallelRunner, Task, TaskResult
from sage.all import ZZ

try:
    import coloredlogs
    coloredlogs.install(level=logging.INFO)
except Exception as e:
    print('E: Package coloredlogs is not installed. No logs will be displayed')


logger = logging.getLogger(__name__)


def get_file_name(params, resdir=None):
    fname = '%s.json' % ('_'.join(map(str, params)),)
    return fname if resdir is None else os.path.join(resdir, fname)


def parameters(config_path, num_bits=112, total_count=40, count=16, resdir=None):
    with open(config_path, 'r') as f:
        params = json.load(f)
        p, curve_seed = params['%s' % num_bits]

    # This logic was written by Sysox3:
    while total_count > 0:
        if total_count < count:
            file_name = get_file_name([total_count, ZZ(p).nbits(), curve_seed], resdir)
            yield {'count': total_count, 'prime': p, 'seed': curve_seed, 'outfile': file_name}
        else:
            file_name = get_file_name([count, ZZ(p).nbits(), curve_seed], resdir)
            yield {'count': count, 'prime': p, 'seed': curve_seed, 'outfile': file_name}

        total_count -= count
        curve_seed = str.format('{:040X}', int(curve_seed, 16) - count)


def main():
    parser = argparse.ArgumentParser(description='Experiment parallelizer')
    parser.add_argument('--tasks', type=int, default=10,
                        help='Number of tasks to run in parallel')
    parser.add_argument('-s', '--sage', default='sage',
                        help='Path to the sage')
    parser.add_argument('--resdir', dest='resdir', default='./results',
                        help='Where to store experiment results')
    parser.add_argument('-c', '--count', type=int, default=10,
                        help='')
    parser.add_argument('-t', '--totalcount', dest='total_count', type=int, default=100,
                        help='')
    parser.add_argument('-b', '--bits', type=int, default=128,
                        help='')
    parser.add_argument('-p', '--configpath', default='parameters.json',
                        help='')
    args = parser.parse_args()
    print(args)

    os.makedirs(args.resdir, exist_ok=True)  # make sure resdir exists

    script_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    wrapper_path = os.path.join(script_path, 'simulations_x962_wrapper.py')

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
        for p in parameters(args.configpath, args.bits, args.total_count, args.count, args.resdir):
            cli = ' '.join(['--%s=%s' % (k, p[k]) for k in p.keys()])
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






