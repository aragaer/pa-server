import json
import logging
import os
import signal
import smtplib
import socket
import time

from behave import *
from nose.tools import eq_, ok_

from utils import LineReader


_LOGGER = logging.getLogger(__name__)


@step('{address} is accepting connections')
def try_connect(context, address):
    sock = socket.socket()
    host, port = address.split(':')
    result = sock.connect_ex((host, int(port)))
    eq_(result, 0, "Send socket: " + os.strerror(result))
    sock.close()


@given('the server is running')
def step_impl(context):
    context.execute_steps('''
    Given %s is accepting connections
      And %s is accepting connections
    ''' % (context.send_address, context.recv_address))


@given('pa is configured to use the server')
def step_impl(context):
    pass


@given('pa is connected to the server')
def step_impl(context):
    host, port = context.recv_address.split(':')
    context.runner.ensure_running("imap-client",
                                  with_args=[host, port,
                                             context.config['pa']['login'],
                                             context.config['pa']['pass']])
    context.add_cleanup(context.runner.terminate, 'imap-client')
    context.add_cleanup(time.sleep, 0.05) # Give it time to expunge
    context.channel = context.runner.get_channel("imap-client")
    context.reader = LineReader(context.channel)


@given('the client is set up correctly')
def step_impl(context):
    context.client_smtp = smtplib.LMTP(context.config['server']['host'],
                                       port=context.config['server']['send'])


@when('I send the \'{action}\' action')
def step_impl(context, action):
    user = context.config['client']['login']
    pa = context.config['pa']['login']
    sender = user+"@human"
    message = json.dumps({'from': user, 'to': pa, 'action': action})
    context.client_smtp.sendmail(sender, pa, b'\r\n'+message.encode())


def timeout(signum, _):
    raise Exception("timeout")


def _get_message(context):
    result = context.reader.readline()
    if not result:
        signal.signal(signal.SIGALRM, timeout)
        signal.alarm(1)
        while True:
            try:
                result = context.reader.readline()
            except:
                break
            if result:
                break
        signal.alarm(0)
    _LOGGER.info("got reply '%s'", result)
    if not result:
        return
    return json.loads(result.decode())


@then('pa receives the \'{event}\' event')
def step_impl(context, event):
    message = _get_message(context)
    ok_(message)
    _LOGGER.info(message)
    eq_(message['action'], event)
