#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Dusan Klinec, ph4r05, 2018
# pip install shellescape sarge

import logging
import signal
import threading
import time
import sys
import os

from shlex import quote
import shellescape
from sarge import Capture, Feeder, run

logger = logging.getLogger(__name__)
SARGE_FILTER_INSTALLED = False


def try_fnc(fnc):
    try:
        fnc()
    except:
        pass
    

class SargeLogFilter(logging.Filter):
    """Filters out debugging logs generated by sarge - output capture. It is way too verbose for debug"""

    def __init__(self, name="", *args, **kwargs):
        self.namex = name
        logging.Filter.__init__(self, *args, **kwargs)

    def filter(self, record):
        if record.levelno != logging.DEBUG:
            return 1

        try:
            # Parse messages are too verbose, skip.
            if record.name == "sarge.parse":
                return 0

            # Disable output processing message - length of one character.
            msg = record.getMessage()
            if "queued chunk of length 1" in msg:
                return 0

            return 1

        except Exception as e:
            logger.error("Exception in log filtering: %s" % (e,))

        return 1


def install_sarge_filter():
    """
    Installs Sarge log filter to avoid long 1char debug dumps
    :return:
    """
    global SARGE_FILTER_INSTALLED
    if SARGE_FILTER_INSTALLED:
        return

    for handler in logging.getLogger().handlers:
        handler.addFilter(SargeLogFilter("hnd"))
    logging.getLogger().addFilter(SargeLogFilter("root"))
    SARGE_FILTER_INSTALLED = True


def sarge_sigint(proc, sig=signal.SIGTERM):
    """
    Sends sigint to sarge process
    :return:
    """
    proc.process_ready.wait()
    p = proc.process
    if not p:  # pragma: no cover
        raise ValueError("There is no subprocess")
    p.send_signal(sig)


def escape_shell(inp):
    """
    Shell-escapes input param
    :param inp:
    :return:
    """
    try:
        inp = inp.decode("utf8")
    except:
        pass

    try:
        return shellescape.quote(inp)
    except:
        pass

    quote(inp)


class AsyncRunner:
    def __init__(self, cmd, args=None, stdout=None, stderr=None, cwd=None, shell=True, env=None):
        self.cmd = cmd
        self.args = args
        self.on_finished = None
        self.on_output = None
        self.on_tick = None
        self.no_log_just_write = False
        self.log_out_during = True
        self.log_out_after = True
        self.stdout = stdout
        self.stderr = stderr
        self.cwd = cwd
        self.shell = shell
        self.env = env
        self.preexec_setgrp = False

        self.using_stdout_cap = True
        self.using_stderr_cap = True
        self.ret_code = None
        self.out_acc = []
        self.err_acc = []
        self.time_start = None
        self.time_elapsed = None
        self.feeder = None
        self.proc = None
        self.is_running = False
        self.was_running = False
        self.terminating = False
        self.thread = None

    def run(self):
        try:
            self.run_internal()
        except Exception as e:
            self.is_running = False
            logger.error("Unexpected exception in runner: %s" % (e,))
        finally:
            self.was_running = True

    def __del__(self):
        self.deinit()

    def deinit(self):
        try_fnc(lambda: self.feeder.close())

        if not self.proc:
            return

        if self.using_stdout_cap:
            try_fnc(lambda: self.proc.stdout.close())

        if self.using_stderr_cap:
            try_fnc(lambda: self.proc.stderr.close())

        try_fnc(lambda: self.proc.close())

    def drain_stream(self, s, block=False, timeout=0.15):
        ret = []
        while True:
            rs = s.read(-1, block, timeout)
            if not rs:
                break
            ret.append(rs)
        return ret

    def run_internal(self):
        def preexec_function():
            os.setpgrp()

        cmd = self.cmd
        if self.shell:
            args_str = (
                " ".join(self.args) if isinstance(self.args, (list, tuple)) else self.args
            )

            if isinstance(cmd, (list, tuple)):
                cmd = " ".join(cmd)

            if args_str and len(args_str) > 0:
                cmd += " " + args_str

        else:
            if self.args and not isinstance(self.args, (list, tuple)):
                raise ValueError("!Shell requires array of args")
            if self.args:
                cmd += self.args

        self.using_stdout_cap = self.stdout is None
        self.using_stderr_cap = self.stderr is None
        self.feeder = Feeder()

        logger.debug("Starting command %s in %s" % (cmd, self.cwd))

        run_args = {}
        if self.preexec_setgrp:
            run_args['preexec_fn'] = preexec_function

        p = run(
            cmd,
            input=self.feeder,
            async_=True,
            stdout=self.stdout or Capture(timeout=0.1, buffer_size=1),
            stderr=self.stderr or Capture(timeout=0.1, buffer_size=1),
            cwd=self.cwd,
            env=self.env,
            shell=self.shell,
            **run_args
        )

        self.time_start = time.time()
        self.proc = p
        self.ret_code = 1
        self.out_acc, self.err_acc = [], []
        out_cur, err_cur = [""], [""]

        def process_line(line, is_err=False):
            dst = self.err_acc if is_err else self.out_acc
            dst.append(line)
            if self.log_out_during:
                if self.no_log_just_write:
                    dv = sys.stderr if is_err else sys.stdout
                    dv.write(line + "\n")
                    dv.flush()
                else:
                    logger.debug("Out: %s" % line.strip())
            if self.on_output:
                self.on_output(self, line, is_err)

        def add_output(buffers, is_err=False, finish=False):
            buffers = [x.decode("utf8") for x in buffers if x is not None and x != ""]
            lines = [""]
            if not buffers and not finish:
                return

            dst_cur = err_cur if is_err else out_cur
            for x in buffers:
                clines = [v.strip("\r") for v in x.split("\n")]
                lines[-1] += clines[0]
                lines.extend(clines[1:])

            nlines = len(lines)
            dst_cur[0] += lines[0]
            if nlines > 1:
                process_line(dst_cur[0], is_err)
                dst_cur[0] = ""

            for line in lines[1:-1]:
                process_line(line, is_err)

            if not finish and nlines > 1:
                dst_cur[0] = lines[-1] or ""

            if finish:
                cline = dst_cur[0] if nlines == 1 else lines[-1]
                if cline:
                    process_line(cline, is_err)

        try:
            while len(p.commands) == 0:
                time.sleep(0.15)

            logger.debug("Program started, progs: %s" % len(p.commands))
            if p.commands[0] is None:
                self.is_running = False
                self.was_running = True
                logger.error("Program could not be started")
                return

            self.is_running = True
            self.on_change()
            out = None
            err = None

            while p.commands[0] and p.commands[0].returncode is None:
                if self.using_stdout_cap:
                    out = p.stdout.read(-1, False)
                    add_output([out], is_err=False)

                if self.using_stderr_cap:
                    err = p.stderr.read(-1, False)
                    add_output([err], is_err=True)

                if self.on_tick:
                    self.on_tick(self)

                p.commands[0].poll()
                if self.terminating and p.commands[0].returncode is None:
                    logger.debug("Terminating by sigint %s" % p.commands[0])
                    sarge_sigint(p.commands[0], signal.SIGTERM)
                    sarge_sigint(p.commands[0], signal.SIGINT)
                    logger.debug("Sigint sent")
                    logger.debug("Process closed")

                # If there is data, consume it right away.
                if (self.using_stdout_cap and out) or (self.using_stderr_cap and err):
                    continue
                time.sleep(0.15)

            logger.debug("Runner while ended")
            p.wait()
            self.ret_code = p.commands[0].returncode if p.commands[0] else -1

            if self.using_stdout_cap:
                try_fnc(lambda: p.stdout.close())
                add_output(self.drain_stream(p.stdout, True), finish=True)

            if self.using_stderr_cap:
                try_fnc(lambda: p.stderr.close())
                add_output(self.drain_stream(p.stderr, True), is_err=True, finish=True)

            self.was_running = True
            self.is_running = False
            self.on_change()

            logger.debug("Program ended with code: %s" % self.ret_code)
            logger.debug("Command: %s" % cmd)

            if self.log_out_after:
                logger.debug("Std out: %s" % "\n".join(self.out_acc))
                logger.debug("Error out: %s" % "\n".join(self.err_acc))

        except Exception as e:
            self.is_running = False
            logger.error("Exception in async runner: %s" % (e,))

        finally:
            self.was_running = True
            self.time_elapsed = time.time() - self.time_start
            try_fnc(lambda: self.feeder.close())
            try_fnc(lambda: self.proc.close())

            if self.on_finished:
                self.on_finished(self)

    def on_change(self):
        pass

    def shutdown(self):
        if not self.is_running:
            return

        self.terminating = True
        time.sleep(1)

        # Terminating with sigint
        logger.debug("Waiting for program to terminate...")
        while self.is_running:
            time.sleep(0.1)
        logger.debug("Program terminated")
        self.deinit()

    def start(self, wait_running=True):
        install_sarge_filter()
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.setDaemon(False)
        self.thread.start()
        self.terminating = False
        if not wait_running:
            self.is_running = True
            return

        self.is_running = False
        while not self.is_running and not self.was_running:
            time.sleep(0.1)
        return self