import time
import unittest

import imaplib2

from unittest.mock import MagicMock, Mock, patch

from client import ImapConnection, ImapIdler


class ConnectionTest(unittest.TestCase):

    _imap = None
    _idler = None
    _messages = None

    def setUp(self):
        patcher = patch('imaplib2.IMAP4')
        self._imap = patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch('client.ImapIdler')
        self._idler = patcher.start()
        self.addCleanup(patcher.stop)

        self._messages = []

    def _on_message(self, message):
        self._messages.append(message)

    def test_create(self):
        conn = ImapConnection("localhost", "login", "pass",
                              onmessage=self._on_message)

        self._imap.assert_called_once_with("localhost")
        self._imap.return_value.login.assert_called_once_with("login", "pass")
        self._imap.return_value.select.assert_called_once_with("INBOX")
        self._idler.assert_called_once_with(self._imap.return_value)

    def test_create_port(self):
        conn = ImapConnection("localhost:8080", "login", "pass",
                              onmessage=self._on_message)

        self._imap.assert_called_once_with("localhost", port=8080)

    def test_start(self):
        conn = ImapConnection("hello", "world", "", None)
        self.addCleanup(conn.stop)

        conn.start()

        self._idler.return_value.start.assert_called_once_with()

    def test_stop(self):
        conn = ImapConnection("hello", "world", "", None)
        conn.stop()

        self._imap.return_value.logout.assert_called_once()
        self._imap.return_value.close.assert_called_once()


class IdlerTest(unittest.TestCase):

    _imap_conn = None
    _idler = None

    def setUp(self):
        self._imap_conn = Mock(spec=imaplib2.IMAP4)
        self._idler = ImapIdler(self._imap_conn)
        self.addCleanup(self._idler.stop)

    def _get_idle_callback(self):
        for _ in range(100):
            if self._imap_conn.idle.called:
                return self._imap_conn.idle.call_args[1]['callback']
            time.sleep(0.001)
        self.fail("idle not called")

    def test_start(self):
        self._idler.dosync = MagicMock()
        self._idler.start()
        idle_cb = self._get_idle_callback()

        self._idler.dosync.assert_not_called()

        idle_cb(None)

        self.assertTrue(self._idler.dosync.called, "idler's dosync is called")

    def test_stop(self):
        self._idler.dosync = MagicMock()
        self._idler.start()
        idle_cb = self._get_idle_callback()

        self._idler.stop()
        idle_cb(None)

        self._idler.dosync.assert_not_called()

    def test_dosync(self):
        self._idler.dosync()
