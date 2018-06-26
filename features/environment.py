#!/usr/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import logging
import os

_LOGGER = logging.getLogger(__name__)
def before_all(context):
    this_dir = os.path.dirname(__file__)
    config = {}
    with open(os.path.join(this_dir, 'server.conf')) as conf:
        for line in conf:
            line = line.strip()
            if line.startswith('#'):
                continue
            key, value = line.split('=')
            config[key] = value
    context.send_address = (config['server'], int(config['send_port']))
    context.recv_address = (config['server'], int(config['recv_port']))
