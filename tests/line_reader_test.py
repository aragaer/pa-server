import unittest

from runner.channel import Channel

from utils import LineReader

class _BytesChannel(Channel):
    def __init__(self):
        self._buf = b''

    def put(self, data):
        self._buf = data
        
    def read(self):
        res = self._buf
        self._buf = b''
        return res

    def write(self, *data):
        pass

    def close(self):
        pass


class LineReaderTest(unittest.TestCase):

    def setUp(self):
        self._chan = _BytesChannel()
        self._reader = LineReader(self._chan)

    def test_read_empty(self):
        line = self._reader.readline()

        self.assertEqual(line, b'')

    def test_read_one_line(self):
        self._chan.put(b'line\n')

        line = self._reader.readline()

        self.assertEqual(line, b'line\n')

    def test_try_read_second_line(self):
        self._chan.put(b'line\n')

        line = self._reader.readline()
        line = self._reader.readline()

        self.assertEqual(line, b'')

    def test_read_one_of_two(self):
        self._chan.put(b'line1\nline2\n')

        line = self._reader.readline()

        self.assertEqual(line, b'line1\n')

    def test_read_two_of_two(self):
        self._chan.put(b'line1\nline2\n')

        line = self._reader.readline()
        line = self._reader.readline()

        self.assertEqual(line, b'line2\n')

    def test_read_incomplete(self):
        self._chan.put(b'line1')

        line = self._reader.readline()

        self.assertEqual(line, b'')

    def test_read_incomplete(self):
        self._chan.put(b'line1')
        self._reader.readline()
        self._chan.put(b'\n')

        line = self._reader.readline()

        self.assertEqual(line, b'line1\n')
