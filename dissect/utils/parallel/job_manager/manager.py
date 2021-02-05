#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Dusan Klinec, ph4r05, 2020
# pip install shellescape sarge

"""
Manager takes care of parallel execution of computation jobs.
Number of tasks to be computed in parallel is set on the initialization and remains
fixed.
"""

import argparse
import json
import logging
import os
import queue
import shlex
import time
import uuid
from typing import List, Optional

from dissect.utils.parallel.job_manager.runner import AsyncRunner

logger = logging.getLogger(__name__)


def try_fnc(fnc):
    try:
        return fnc()
    except:
        pass


def get_runner(cli, cwd=None, env=None):
    async_runner = AsyncRunner(cli, cwd=cwd, shell=False, env=env)
    async_runner.log_out_after = False
    async_runner.preexec_setgrp = True
    return async_runner


def is_task_done(file_path):
    if not os.path.isfile(file_path):
        return False
    with open(file_path, 'r') as f:
        content = json.load(f)
        if not isinstance(content, dict):
            return False
    return True


class Task:
    def __init__(self, wrapper, params, tid=None):
        self.wrapper = wrapper
        self.params = params
        self.idx = tid if tid else str(uuid.uuid4())

        self.failed_attempts = 0  # number of attempts failed
        self.skip = False  # should skip if found in the queue?
        self.skipped = False  # skipped


class TaskResult:
    def __init__(self, job, ret_code, stderr=None):
        self.job = job  # type: Task
        self.ret_code = ret_code
        self.stderr = stderr


class ParallelRunner:
    def __init__(self):
        self.args = None
        self.parallel_tasks = None
        self.job_feeder = None  # function, returning task
        self.cb_job_finished = None
        self.cb_job_prerun = None
        self.last_job_id = 0

        self.bool_wrapper = None
        self.tick_time = 0.15
        self.job_iterator = None
        self.job_queue = queue.Queue(maxsize=0)
        self.runners = []  # type: List[Optional[AsyncRunner]]
        self.comp_jobs = []  # type: List[Optional[Task]]
        self.results = []

    def run_job(self, cli):
        async_runner = get_runner(shlex.split(cli))

        logger.info("Starting async command %s" % cli)
        async_runner.start()

        while async_runner.is_running:
            time.sleep(1)
        logger.info("Async command finished")

    def on_finished(self, job: Task, runner: AsyncRunner, idx: int):
        stderr = ("\n".join(runner.err_acc)).strip()
        br = TaskResult(job, runner.ret_code, stderr)  # results

        if runner.ret_code != 0:
            logger.warning("Return code of job %s is %s" % (idx, runner.ret_code))
            job.failed_attempts += 1

        if self.cb_job_finished:
            self.cb_job_finished(br)

    def get_num_running(self):
        return sum([1 for x in self.runners if x])

    def queue_threshold(self):
        return self.parallel_tasks * 100

    def pull_jobs(self):
        cur_jobs = [x for _, x in zip(range(self.queue_threshold()), self.job_iterator) if x is not None]
        for i, j in enumerate(cur_jobs):
            j.idx = self.last_job_id + i

        self.last_job_id += len(cur_jobs)
        for j in cur_jobs:
            self.job_queue.put_nowait(j)

    def enqueue(self, j: Task):
        self.job_queue.put_nowait(j)

    def work(self):
        self.job_iterator = self.job_feeder()
        self.runners = [None] * self.parallel_tasks  # type: List[Optional[AsyncRunner]]
        self.comp_jobs = [None] * self.parallel_tasks  # type: List[Optional[Task]]
        self.pull_jobs()

        logger.info("Starting Experiment runner, threads: %s, jobs: %s"
                    % (self.parallel_tasks, self.job_queue.qsize()))

        while not self.job_queue.empty() or sum([1 for x in self.runners if x is not None]) > 0:
            time.sleep(self.tick_time)

            # Realloc work
            for i in range(len(self.runners)):
                if self.runners[i] is not None and self.runners[i].is_running:
                    continue

                was_empty = self.runners[i] is None
                if not was_empty:
                    self.job_queue.task_done()
                    logger.info("Task %d done, job queue size: %d, running: %s"
                                % (i, self.job_queue.qsize(), self.get_num_running()))
                    self.on_finished(self.comp_jobs[i], self.runners[i], i)

                # Start a new task, if any
                try:
                    job = self.job_queue.get_nowait()  # type: Task
                except queue.Empty:
                    self.runners[i] = None
                    continue

                if self.cb_job_prerun:
                    self.cb_job_prerun(job)

                if job.skip:
                    job.skipped = True
                    continue

                job.skipped = False
                params = job.params if isinstance(job.params, str) else ' '.join(job.params)
                cli = '%s %s' % (job.wrapper, params)
                self.comp_jobs[i] = job
                self.runners[i] = get_runner(shlex.split(cli))
                logger.info("Starting async command %s, %s" % (job.idx, cli))
                self.runners[i].start()
                logger.info("Runner %s started, job queue size: %d, running: %s"
                            % (i, self.job_queue.qsize(), self.get_num_running()))

                # Re-fill job queue with some data
                if self.job_queue.qsize() < self.queue_threshold() / 2:
                    self.pull_jobs()

    def process_input(self):
        """
        Design options:
         1. This is the main executor
          - Need to provide exp scripts paths, load dynamically.

         2. Users experiment definition script is the main executor.
          - Manager used as a library.
          - Need to reduce boilerplate for the executor, argparse, loading, ...

        :return:
        """
        raise ValueError('Standalone execution is not implemented yet')

    def main(self):
        logger.debug('App started')

        parser = self.argparser()
        self.args = parser.parse_args()
        self.parallel_tasks = self.args.tasks or try_fnc(lambda: int(os.getenv('EC_PARALLEL', None))) or 1
        self.process_input()
        self.work()

    def argparser(self):
        parser = argparse.ArgumentParser(description='Parallelization of jobs!')
        parser.add_argument('-t', '--tasks', type=int,
                            help='Maximal number of parallel tasks')
        parser.add_argument('-w', '--wrapper',
                            help='Wrapper script absolute path')

        parser.add_argument('-ei', '--exp-import',
                            help='Experiment definition script import path')
        parser.add_argument('-ep', '--exp-path',
                            help='Experiment definition script path')

        parser.add_argument('-c', '--config', type=int,
                            help='Experiment configuration file.'
                                 'Passed to job-gen to generate individual jobs & tasks.')
        return parser


def main():
    pr = ParallelRunner()
    return pr.main()


if __name__ == '__main__':
    main()
