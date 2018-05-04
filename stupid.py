import io
import logging

from twisted.cred import checkers, credentials
from twisted.mail import imap4
from zope.interface import implementer

import queues

_LOGGER = logging.getLogger(__name__)

@implementer(imap4.IAccount)
class StupidUserAccount:
    def __init__(self, cache):
        self.cache = cache
    
    def listMailboxes(self, ref, wildcard):
        return [(0, "Inbox")]

    def select(self, path, rw=True):
        return StupidImapMailbox("Inbox", self.cache)

    def close(self):
        return True

    def create(self, path):
        return False

    def delete(self, path):
        return False

    def rename(self, oldname, newname):
        return False

    def isSubscribed(self, path):
        return True

    def subscribe(self, path):
        return True

    def unsubscribe(self, path):
        return True


@implementer(imap4.IMailbox)
class StupidImapMailbox:

    def __init__(self, folder, cache):
        _LOGGER.debug("Fetching: %s", folder)
        self.folder = folder
        self.user = cache.get('username')
        self.cache = cache
        self.listeners = []

    def getHierarchicalDelimiter(self):
        return b':'

    def getFlags(self):
        return [r'\Seen', r'\Deleted']

    def getMessageCount(self):
        return queues.count(self.user)

    def getRecentCount(self):
        return 0

    def getUnseenCount(self):
        return queues.count(self.user)

    def isWriteable(self):
        return True

    def getUIDValidity(self):
        return 0

    def getUID(self, messageNum):
        _LOGGER.debug("get uid")
        raise imap4.MailboxException("Not implemented")

    def getUIDNext(self):
        _LOGGER.debug("get uid next")
        raise imap4.MailboxException("Not implemented")

    def fetch(self, messages, uid):
        _LOGGER.debug("FETCH :: %s :: %s :: %s", self.folder, messages, uid)
        if uid:
            _LOGGER.debug("fetch by uid")
            raise imap4.MailboxException("Not implemented")
        result = []
        messages.last = queues.count(self.user)
        for seq_n in messages:
            msg_text, seen = queues.get(self.user, seq_n)
            if msg_text is None:
                continue
            msg = {"text": msg_text, 'seen': seen}
            _LOGGER.debug("FETCH :: %s", msg)
            msg['counter'] = seq_n
            mail = StupidImapMessage(msg, self.cache)
            result.append((seq_n, mail))
        return result

    def addListener(self, listener):
        self.listeners.append(listener)
        return True

    def removeListener(self, listener):
        self.listeners.remove(listener)
        return True

    def requestStatus(self, names):
        return imap4.statusRequestHelper(self, names)

    def addMessage(self, msg, flags=None, date=None):
        _LOGGER.debug("destroy")
        raise imap4.MailboxException("Not implemented")

    def store(self, messages, flags, mode, uid):
        _LOGGER.debug("STORE: %s :: %s :: %s :: %s",
                      messages, flags, mode, uid)
        if uid:
            _LOGGER.debug("store by uid")
            raise imap4.MailboxException("Not implemented")
        if mode == -1:
            raise imap4.MailboxException("Can not unmark")
        seen_flag = r'\Seen' in flags
        deleted_flag = r'\Deleted' in flags
        if seen_flag ^ deleted_flag:
            _LOGGER.debug("Seen %s, Deleted %s", seen_flag, deleted_flag)
            raise imap4.MailboxException("Can only mark both seen and deleted")
        messages.last = queues.count(self.user)
        for seq_n in messages:
            queues.mark_seen(self.user, seq_n)

    def expunge(self):
        _LOGGER.debug("expunge")
        queues.clean(self.user)

    def destroy(self):
        _LOGGER.debug("destroy")
        raise imap4.MailboxException("Not implemented")

@implementer(imap4.IMessage)
class StupidImapMessage:

    def __init__(self, info, cache):
        self.info = info
        self.cache = cache

    def getUID(self):
        return self.info['counter']

    def getFlags(self):
        if self.info['seen']:
            return [r'\Seen', r'\Deleted']
        return []

    def getInternalDate(self):
        return "1970-01-01"

    def getHeaders(self, negate, *names):
        user_name = self.cache.get("username")
        uname = user_name
        sender_name = "brain"
        sname = "pa"

        headers = {
            "to": "%s <%s@pa.com>" % (user_name, uname),
            "from": "%s <%s@pa.com>" % (sname, sender_name),
            "delivery-date": "%s" % "1970-01-01", 
            "date": "%s" % "1970-01-01", 
            "subject": "message",
            "message-id": "test",
            "content-type": 'text/plain; charset="UTF-8"',
            "content-transfer-encoding": "quoted-printable",
            "mime-version": "1.0",
        }

        result = {}
        for k, v in headers.items():
            if (k in names) == negate:
                result[k] = v

        return result

    def getBodyFile(self):
        return io.BytesIO(self.info['text'].encode())

    def getSize(self):
        return len(self.info['text'])

    def isMultipart(self):
        return False

    def getSubPart(self, part):
        raise imap4.MailboxException("getSubPart not implemented")


@implementer(checkers.ICredentialsChecker)
class StupidCredentialsChecker:
    credentialInterfaces = (credentials.IUsernamePassword,)

    def __init__(self, cache):
        self.cache = cache

    def requestAvatarId(self, credentials):
        self.cache.set('username', credentials.username.decode())
        return credentials.username
