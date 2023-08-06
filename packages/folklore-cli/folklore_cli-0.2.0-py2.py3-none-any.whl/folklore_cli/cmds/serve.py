# -*- coding: utf-8 -*-

"""Serve a folklore thrift service.

Usage:
    folklore serve [<gunicorn_args>...]
"""

import sys


def run(args):
    from ..runner import AppRunner
    from folklore_ext import ext
    sys.argv = ['folklore serve'] + args
    # Delegate to gunicorn
    runner = AppRunner()
    app_runner_ext = ext['app-runner']

    if app_runner_ext:
        runner_ext = app_runner_ext(runner)
        runner.cfg.set('when_ready', lambda x: runner_ext.on_start())
        runner.cfg.set('on_exit', lambda x: runner_ext.on_exit())
    runner.run()
