import logging

_QUEUES = {}
_LOGGER = logging.getLogger(__name__)

class Box:

    def __init__(self):
        self._msgs = []
        self._to_delete = set()

    def put(self, data):
        self._msgs.append(data)

    def get(self, msg_seq_n):
        num = msg_seq_n-1
        return self._msgs[num], (num in self._to_delete)

    def drop(self, msg_seq_n):
        self._msgs.pop(msgs_seq_n-1)

    @property
    def count(self):
        return len(self._msgs)

    def mark_seen(self, msg_seq_n):
        self._to_delete.add(msg_seq_n-1)

    def clean(self):
        tmp = []
        for i, msg in enumerate(self._msgs):
            if i not in self._to_delete:
                tmp.append(msg)
        self._msgs = tmp
        self._to_delete.clear()

def put(user, data):
    if user not in _QUEUES:
        _QUEUES[user] = Box()
    _QUEUES[user].put(data)

def get(user, msg_seq_n):
    if user in _QUEUES:
        return _QUEUES[user].get(msg_seq_n)
    return None, False

def count(user):
    if user not in _QUEUES:
        return 0
    return _QUEUES[user].count

def drop(user, msg_seq_n):
    if user in _QUEUES:
        _QUEUES[user].drop(msg_seq_n)

def mark_seen(user, msg_seq_n):
    if user in _QUEUES:
        _QUEUES[user].mark_seen(msg_seq_n)

def clean(user):
    if user in _QUEUES:
        _QUEUES[user].clean()
