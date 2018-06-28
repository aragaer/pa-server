import logging

import imaplib2


_LOGGER = logging.getLogger(__name__)


class ImapConnection:
    def __init__(self, host_port, login, password, onmessage):
        if ':' in host_port:
            host, port = host_port.split(':')
            self._conn = imaplib2.IMAP4(host, port=int(port))
        else:
            self._conn = imaplib2.IMAP4(host_port)
        self._conn.login(login, password)
        self._conn.select("INBOX")
        self._idler = ImapIdler(self._conn)

    def start(self):
        self._idler.start()

    def stop(self):
        self._conn.close()
        self._conn.logout()


class ImapIdler:
    def __init__(self, conn):
        self._conn = conn
        self._running = False

    def stop(self):
        self._running = False

    def start(self):
        def cb(_):
            if self._running:
                self.dosync()

        self._running = True
        self._conn.idle(callback=cb)

    def dosync(self):
        pass
