#!/usr/bin/python3

import configparser
import os


def before_all(context):
    this_dir = os.path.dirname(__file__)
    config = configparser.ConfigParser()
    config.read(os.path.join(this_dir, 'server.conf'))

    srv = config['server']
    context.send_address = srv['host']+":"+srv['send']
    context.recv_address = srv['host']+":"+srv['recv']
