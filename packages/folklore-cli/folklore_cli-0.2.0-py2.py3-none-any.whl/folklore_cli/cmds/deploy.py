# -*- coding: utf-8 -*-

"""Deploy a Folklore app.

Usage:
    folklore deploy <target> [options] [(-- <ansible_args>...)]
    folklore deploy -- <ansible_args>...
    folklore deploy -h | --help

Options:
    -t, --tags TAGS  Only run tasks with these tags
    -p, --play PLAY  Specify a different playbook
    -h, --help       Show this message and exit

Example:

    Simple deploy:

        folklore deploy testing

    Deploy a subject:

        folklore deploy testing -t cron

    Specify other playbooks:

        folklore deploy testing -p system.yml
"""

import schema
from ._base import parse_args


def run(args):
    args = parse_args('deploy', __doc__, args, {
        '--tags': schema.Or(None, str),
        '--play': schema.Or(None, str),
        '<target>': schema.Or(None, lambda x: x != '--',
                              error='Invalid value of target'),
        '<ansible_args>': list
    })

    from ..deploy import start

    try:
        start(args)
    except Exception as e:
        exit('Fail to deploy: {}'.format(e))
