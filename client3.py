#!/usr/bin/env python3
"Uses runner and pa-client to read from imap"
import atexit
import configparser
import logging
import os
import sys

from runner import Runner


_LOGGER = logging.getLogger(__name__)
this_dir = os.path.dirname(__file__)
conf_path = os.path.join(this_dir, 'features', 'server.conf')
config = configparser.ConfigParser()
config.read(conf_path)

srv = config['server']
usr = config['pa']

def timeout(signum, _):
    raise Exception("timeout")


def _get_message(channel):
    message = None
    while True:
        try:
            message = channel.read()
        except:
            break
        if message:
            _LOGGER.debug("Message %s", message)
            break
    _LOGGER.debug("Got message %s", message)
    if message is not None:
        _LOGGER.info("got reply '%s'", message)
        return message
    _LOGGER.info("got no reply")


def main():
    runner = Runner()
    runner.update_config({'imap-client':
                          {'command': ' '.join(['pa-client',
                                                srv['host'],
                                                srv['recv'],
                                                usr['login'],
                                                usr['pass']]),
                           'type': 'stdio'}})
    atexit.register(runner.terminate, 'imap-client')
    runner.ensure_running('imap-client')
    while True:
        message = _get_message(runner.get_channel('imap-client'))
        if not message:
            break
        print(message.decode(), end='')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    main()
