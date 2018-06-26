@given(u'the server is running')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given the server is running')


@given(u'pa is configured to use the server')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given pa is configured to use the server')


@given(u'pa is connected to the server')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given pa is connected to the server')


@given(u'the client is set up correctly')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given the client is set up correctly')


@when(u'I send the \'ping\' action')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I send the \'ping\' action')


@then(u'pa receives the \'ping\' event')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then pa receives the \'ping\' event')
