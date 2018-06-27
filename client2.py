#!/usr/bin/env python3
import getpass
import logging
import time

from threading import Event, Thread

import imaplib2


class Idler:
    def __init__(self, conn):
        self.thread = Thread(target=self.idle)
        self.M = conn
        self.event = Event()
        self.needsync = False

    def start(self):
        self.thread.start()

    def stop(self):
        self.event.set()

    def join(self):
        self.thread.join()

    def dosync(self):
        self.M.select()
        typ, data = self.M.search(None, 'ALL')
        for num in data[0].split():
            typ, data = self.M.fetch(num, '(RFC822)')
            print(num, data[0][1].strip())
            self.M.store(num, "+FLAGS", r'\Seen \Deleted')
            self.M.expunge()

    def idle(self):
        while True:
            if self.event.isSet():
                return
            self.needsync = False

            def callback(args):
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()

            self.M.idle(callback=callback)
            self.event.wait()

            if self.needsync:
                self.event.clear()
                self.dosync()


def main():
    M = imaplib2.IMAP4("netbook-eth", port=8007)
    M.login("aragaer","secret")
    M.select("INBOX")
    typ, data = M.search(None, 'ALL')
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        print(num, data[0][1].strip())
        M.store(num, "+FLAGS", r'\Seen \Deleted')
    M.expunge()
    idler = Idler(M)
    idler.start()

    while True:
        time.sleep(1*60)

    idler.stop()
    idler.join()
    M.close()
    M.logout()


if __name__ == '__main__':
    main()
