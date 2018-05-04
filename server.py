#!/usr/bin/env python3
import logging
import sys

from aiosmtpd.controller import Controller
from twisted.mail import imap4
from twisted.internet import asyncioreactor, reactor, protocol
from twisted.cred import portal
from zope.interface import implementer

import queues
from stupid import StupidUserAccount, StupidCredentialsChecker

_LOGGER = logging.getLogger(__name__)

class ObjCache():
    def __init__(self):
        self.cache = {}

    def get(self, item):
        return self.cache[item]

    def set(self, item, value):
        self.cache[item] = value


@implementer(portal.IRealm)
class MailUserRealm:
    def __init__(self, cache):
        self.cache = cache

    def requestAvatar(self, avatarId, mind, *interfaces):
        if imap4.IAccount in interfaces:
            avatar = StupidUserAccount(self.cache)
            logout = lambda: None
            return imap4.IAccount, avatar, logout
        raise KeyError("None of the requested interfaces is supported")


class IMAPServerProtocol(imap4.IMAP4Server):
    "Subclass of imap4.IMAP4Server that adds debugging."

    def lineReceived(self, line):
        _LOGGER.debug("CLIENT: %s", line.decode())
        super().lineReceived(line)

    def sendLine(self, line):
        super().sendLine(line)
        _LOGGER.debug("SERVER: %s", line.decode())


class IMAPFactory(protocol.Factory):
    portal = None # placeholder

    def buildProtocol(self, address):
        p = IMAPServerProtocol()
        p.portal = self.portal
        p.factory = self
        return p

class SMTPHandler:
    
    async def handle_RCPT(self, server, session,
                          envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        _LOGGER.info('Message from %s', envelope.mail_from)
        _LOGGER.info('Message for %s', envelope.rcpt_tos)
        _LOGGER.info('Message data:')
        data = envelope.content.decode('utf8', errors='replace').strip()
        _LOGGER.info(data)
        _LOGGER.info('End of message')
        for user in envelope.rcpt_tos:
            queues.put(user, data)
        return '250 Message accepted for delivery'

def main():
    cache = ObjCache()
    logging.basicConfig(stream=sys.stderr,
                        level=logging.DEBUG)

    logging.getLogger('mail.log').setLevel(logging.INFO)

    p = portal.Portal(MailUserRealm(cache))
    p.registerChecker(StupidCredentialsChecker(cache))

    factory = IMAPFactory()
    factory.portal = p

    reactor.listenTCP(8007, factory)
    controller = Controller(SMTPHandler(),
                            hostname="127.0.0.1",
                            port=8006)
    controller.start()
    reactor.run()


if __name__ == "__main__":
    main()
