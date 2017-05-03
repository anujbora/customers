from behave import *
import json
import server as server

@given(u'the following customers')
def step_impl(context):
    server.data_reset()
    for row in context.table:
        server.data_load({"first_name": row['first_name'],"last_name": row['last_name'], "id":row['id'], 
        "gender":row['gender'], "age":row['age'],"email":row['email'],"address_line1":row['address_line1'],
        "address_line2":row['address_line2'],"phonenumber":row['phonenumber']})

@when(u'I visit the home page')
def step_impl(context):
    context.resp = context.app.get('/')

@then(u'I should see "{message}"')
def step_impl(context,message):
    assert message in context.resp.data

@then(u'I should not see "{message}"')
def step_impl(context,message):
    assert message not in context.resp.data

@when(u'I visit "{url}"')
def step_impl(context,url):
    context.resp = context.app.get(url)
    assert context.resp.status_code == 200

@when(u'I add a new customer "Lionel Messi"')
def step_impl(context):
    new_customer =  {"first_name": "Lionel", "last_name": "Messi", "gender": "M",
    "age": "29", "email" : "messi@barca.com", "address_line1": "Camp Nou",
    "address_line2": "Barcelona", "phonenumber": "666"}
    new_data = json.dumps(new_customer)
    context.resp = context.app.post('/customers',data = new_data,content_type='application/json')
    assert context.resp.status_code == 201


@when(u'I retrieve "{url}" with id "{id}"')
def step_impl(context,url,id):
    target_url = '/{}/{}'.format(url, id)
    context.resp = context.app.get(target_url)
    assert context.resp.status_code == 200

@when(u'I change "{key}" to "{value}"')
def step_impl(context,key,value):
    data = json.loads(context.resp.data)
    data[key] = value
    context.resp.data = json.dumps(data)    

@when(u'I update "{url}" with id "{id}"')
def step_impl(context,url,id):
    target_url = '/{}/{}'.format(url,id)
    context.resp = context.app.put(target_url,data=context.resp.data,content_type='application/json')
    assert context.resp.status_code == 200

@when(u'I delete "{url}" with id "{id}"')
def step_impl(context,url,id):
    target_url = '/{}/{}'.format(url, id)
    context.resp = context.app.delete(target_url)
    assert context.resp.status_code == 204
    assert context.resp.data is ""

@when(u'I query "{url}" by "{field}" with value "{value}"')
def step_impl(context,url,field,value):
    target_url = '/{}?{}={}'.format(url,field,value)
    context.resp = context.app.get(target_url)
    assert context.resp.status_code == 200

@then(u'I should see "{count}" rows of data')
def step_impl(context,count):
    data = json.loads(context.resp.data)
    count = int(count)
    assert len(data) == count

@then(u'I should have "active" as "{value}"')
def step_impl(context,value):
    data = json.loads(context.resp.data)
    #print(data)
    assert data['active'] == value        

@when(u'I "{action}" "{url}" with id "{id}"')
def step_impl(context,action,url,id):
    target_url = '/{}/{}/{}'.format(url,id,action)
    #target_url = '/customers/1/deactivate'
    context.resp = context.app.put(target_url,data=context.resp.data,content_type='application/json')
    print(target_url)
    print(context.resp.status_code)
    #assert context.resp.status_code == 200
