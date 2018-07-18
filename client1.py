#!/usr/bin/env python3
"Read all queued messages from imap and bail out"
import configparser
import imaplib
import os

this_dir = os.path.dirname(__file__)
conf_path = os.path.join(this_dir, 'features', 'server.conf')

config = configparser.ConfigParser()
config.read(conf_path)

srv = config['server']
usr = config['pa']

def main():
    M = imaplib.IMAP4(host=srv['host'], port=srv['recv'])
    M.login(usr['login'], usr['pass'])
    M.select()
    typ, data = M.search(None, 'ALL')
    for num in data[0].split():
        num = num.decode()
        typ, data = M.fetch(num, '(RFC822.TEXT)')
        print(num, data[0][1].decode().strip())
        M.store(num, "+FLAGS", r'\Seen \Deleted')
    M.close()
    M.logout()

if __name__ == '__main__':
    main()
