import os
import socket

from behave import *
from nose.tools import eq_


def try_connect(address):
    sock = socket.socket()
    result = sock.connect_ex(address)
    eq_(result, 0, "Send socket: " + os.strerror(result))
    sock.close()


@given('the server is running')
def step_impl(context):
    try_connect(context.send_address)
    raise NotImplementedError('STEP: Given the server is running')


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
