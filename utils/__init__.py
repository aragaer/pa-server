class LineReader:

    def __init__(self, chan):
        self._chan = chan
        self._buf = b''

    def readline(self):
        eol = self._buf.find(b'\n')
        if eol == -1:
            self._buf += self._chan.read()
            eol = self._buf.find(b'\n')
        result, self._buf = self._buf[:eol+1], self._buf[eol+1:]
        return result
