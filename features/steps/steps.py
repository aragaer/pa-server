import os
import socket

from behave import *
from nose.tools import eq_


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
    raise NotImplementedError('STEP: Given pa is configured to use the server')


@given('pa is connected to the server')
def step_impl(context):
    raise NotImplementedError('STEP: Given pa is connected to the server')


@given('the client is set up correctly')
def step_impl(context):
    raise NotImplementedError('STEP: Given the client is set up correctly')


@when('I send the \'ping\' action')
def step_impl(context):
    raise NotImplementedError('STEP: When I send the \'ping\' action')


@then('pa receives the \'ping\' event')
def step_impl(context):
    raise NotImplementedError('STEP: Then pa receives the \'ping\' event')
