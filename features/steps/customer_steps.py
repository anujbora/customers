from behave import *
import json
import server as server

@given(u'the following customers')
def step_impl(context):
    context.app = server.app.test_client()
    context.server = server

@when(u'I visit the home page')
def step_impl(context):
    context.resp = context.app.get('/')

@then(u'I should see title as "{message}"')
def step_impl(context,message):
    assert message in context.resp.data

@then(u'I should not see title as "{message}"')
def step_impl(context,message):
    assert message not in context.resp.data

@when(u'I visit "customers"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I visit "customers"')

@then(u'I should see "{value}" in "{field}')
def step_impl(context,value,field):
    raise NotImplementedError(u'STEP: Then I should see "Jackie"')

@when(u'I visit "customers/2"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I visit "customers/2"')

@when(u'I add a new customer "Lionel Messi"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I add a new customer "Lionel Messi"')

@when(u'I retrieve "customers" with id "1"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I retrieve "customers" with id "1"')

@when(u'I change "address_line1" to "Nariman Point"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I change "address_line1" to "Nariman Point"')

@when(u'I update "customers" with id "2"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I update "customers" with id "2"')

@when(u'I delete "customers" with id "3"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I delete "customers" with id "3"')

@then(u'I should not see "{value}" in "{field}"')
def step_impl(context,value,field):
    raise NotImplementedError(u'STEP: Then I should not see "Maria"')

@when(u'I query by "phonenumber" "420420"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I query by "phonenumber" "420420"')

@when(u'I query by "phonenumber" "111111"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I query by "phonenumber" "111111"')

@then(u'I should see "0" rows of data')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should see "0" rows of data')

@when(u'I retrieve "customers" with id "2"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I retrieve "customers" with id "2"')

@then(u'I should see "active" as "False"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should see "active" as "False"')

@when(u'I "activate" "customers" with id "2"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I "activate" "customers" with id "2"')

@then(u'I should see "active" as "True"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should see "active" as "True"')

@when(u'I "deactivate" "customers" with id "1"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I "deactivate" "customers" with id "1"')
