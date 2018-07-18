#!/usr/bin/env python3
"Uses runner and pa-client to read from imap"
import atexit
import configparser
import os

from runner import Runner

from utils import LineReader


this_dir = os.path.dirname(__file__)
conf_path = os.path.join(this_dir, 'features', 'server.conf')
config = configparser.ConfigParser()
config.read(conf_path)

srv = config['server']
usr = config['pa']

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
    reader = LineReader(runner.get_channel('imap-client'))
    while True:
        message = reader.readline()
        if message:
            print(message.decode(), end='')

if __name__ == '__main__':
    main()
