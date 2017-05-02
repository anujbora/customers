# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY gender, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
from redis import Redis
from redis.exceptions import ConnectionError
from flask import Flask, Response, jsonify, request, json, url_for, make_response
from customers import Customer
from flasgger import Swagger
from flask_api import status

# Create Flask applifion
app = Flask(__name__)
app.config['LOGGING_LEVEL'] = logging.INFO

debug = (os.getenv('DEBUG', 'False') == 'True')
port = os.getenv('PORT', '5000')

# Configure Swagger before initilaizing it
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
        {
            "version": "1.0.0",
            "title": "Customers | NYU DevOps Spring 2017",
            "description": "Customers REST API",
            "endpoint": 'v1_spec',
            "route": '/v1/spec'
        }
    ]
}

# Initialize Swagger after configuring it
Swagger(app)

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    # data = '{first_name: <string>, last_name:<string>,gender:<string>,age:<string>,email:<string>,address_line1:<string>,address_line2:<string>,phonenumber:<string>}'
    # url = request.base_url + 'customers' # url_for('list_customers')
    # return jsonify(name='customer Demo REST API Service', version='1.0', url=url, data=data), HTTP_200_OK
    return app.send_static_file('index.html')

######################################################################
# SEARCH by keyword
######################################################################
@app.route('/customers/search-keyword/<string:keyword>', methods=['GET'])
def search_by_keyword(keyword):
    """
    Retrieve all customers for the given keyword
    This endpoint will return customers which match given keyword
    ---
    tags:
      - Customers
    produces:
      - application/json
    parameters:
      - name: keyword
        in: path
        description: the keyword to match for returning customers information
        type: string
        required: true
    responses:
      200:
        description: An array of customers
        schema:
          type: array
          items:
            schema:
              id: Customer
              properties:
                id:
                  type: integer
                  description: unique id assigned internally by service
                active:
                  type: boolean
                  description: the status of customer whether it is currently active (true) or not (false)
                address_line1:
                  type: string
                  description: address line 1 of the customer
                address_line2:
                  type: string
                  description: address line 2 of the customer
                age:
                  type: integer
                  description: age of the customer
                email:
                  type: string
                  description: email address of the customer
                first_name:
                  type: string
                  description: first name of the customer
                last_name:
                  type: string
                  description: last name of the customer
                gender:
                  type: string
                  description: gender of the customer
                phonenumber:
                  type: string
                  description: phone number of the customer
    """
    results = []
    results.extend(Customer.search_in_age(redis, keyword))
    results.extend(Customer.search_in_first_name(redis, keyword))
    results.extend(Customer.search_in_last_name(redis, keyword))
    results.extend(Customer.search_in_email(redis, keyword))
    results.extend(Customer.search_in_address_line1(redis, keyword))
    results.extend(Customer.search_in_address_line2(redis, keyword))
    results.extend(Customer.search_in_phonenumber(redis, keyword))
    final_results = []
    list_ids = []
    for res in results:
        if res.id not in list_ids:
            final_results.append(res)
            list_ids.append(res.id)
    answer = [Customer.serialize(customer) for customer in final_results]
    return make_response(jsonify(answer), HTTP_200_OK)

######################################################################
# ACTIVATE a customer
######################################################################
@app.route('/customers/activate/<int:id>', methods=['PUT'])
def activate_customer(id):
    """
    Activate a customer with given ID
    This endpoint will activate the customer with given ID
    ---
    tags:
      - Customers
    produces:
      - application/json
    parameters:
      - name: id
        in: path
        description: the id to match for activating customer
        type: integer
        required: true
    responses:
      200:
        description: Customer activated
        schema:
          id: Customer
          properties:
            id:
              type: integer
              description: unique id assigned internally by service
            active:
              type: boolean
              description: the status of customer whether it is currently active (true in this case)
            address_line1:
              type: string
              description: address line 1 of the customer
            address_line2:
              type: string
              description: address line 2 of the customer
            age:
              type: integer
              description: age of the customer
            email:
              type: string
              description: email address of the customer
            first_name:
              type: string
              description: first name of the customer
            last_name:
              type: string
              description: last name of the customer
            gender:
              type: string
              description: gender of the customer
            phonenumber:
              type: string
              description: phone number of the customer
      404:
        description: error, Customer was not found
    """
    customer = Customer.find(redis, id)
    if customer:
		customer.active = True
		customer.save(redis)
		message = customer.serialize()
		rc = HTTP_200_OK
    else:
        message = { 'error' : 'Customer %s was not found' % id }
        rc = HTTP_404_NOT_FOUND
    return make_response(jsonify(message), rc)

######################################################################
# DEACTIVATE a customer
######################################################################
@app.route('/customers/deactivate/<int:id>', methods=['PUT'])
def deactivate_customer(id):
    """
    Deactivate a customer with given ID
    This endpoint will deactivate the customer with given ID
    ---
    tags:
      - Customers
    produces:
      - application/json
    parameters:
      - name: id
        in: path
        description: the id to match for deactivating customer
        type: integer
        required: true
    responses:
      200:
        description: Customer deactivated
        schema:
          id: Customer
          properties:
            id:
              type: integer
              description: unique id assigned internally by service
            active:
              type: boolean
              description: the status of customer whether it is currently active (false in this case)
            address_line1:
              type: string
              description: address line 1 of the customer
            address_line2:
              type: string
              description: address line 2 of the customer
            age:
              type: integer
              description: age of the customer
            email:
              type: string
              description: email address of the customer
            first_name:
              type: string
              description: first name of the customer
            last_name:
              type: string
              description: last name of the customer
            gender:
              type: string
              description: gender of the customer
            phonenumber:
              type: string
              description: phone number of the customer
      404:
        description: error, Customer was not found
    """
    customer = Customer.find(redis, id)
    if customer:
		customer.active = False
		customer.save(redis)
		message = customer.serialize()
		rc = HTTP_200_OK
    else:
        message = { 'error' : 'Customer %s was not found' % id }
        rc = HTTP_404_NOT_FOUND
    return make_response(jsonify(message), rc)

######################################################################
# LIST ALL customers
######################################################################
@app.route('/customers', methods=['GET'])
def list_customers():
    """
    Retrieve all customers or the customers which match given parameter(s)
    This endpoint will return customers which match given parameter(s)
    ---
    tags:
      - Customers
    description: The customers endpoint allows you to query customers
    produces:
      - application/json
    parameters:
      - name: email
        in: query
        description: the email to match for returning customers information
        type: string
        required: false
      - name: last-name
        in: query
        description: the last name to match for returning customers information
        type: string
        required: false
      - name: first-name
        in: query
        description: the first name to match for returning customers information
        type: string
        required: false
      - name: age
        in: query
        description: the age to match for returning customers information
        type: integer
        required: false
      - name: gender
        in: query
        description: the gender to match for returning customers information
        type: string
        required: false
      - name: address-line1
        in: query
        description: the address line 1 to match for returning customers information
        type: string
        required: false
      - name: address-line2
        in: query
        description: the address line 2 to match for returning customers information
        type: string
        required: false
      - name: phonenumber
        in: query
        description: the phone number to match for returning customers information
        type: string
        required: false
      - name: active
        in: query
        description: the status of customer to match for returning customers information
        type: boolean
        required: false
    responses:
      200:
        description: An array of customers
        schema:
          type: array
          items:
            schema:
              id: Customer
              properties:
                id:
                  type: integer
                  description: unique id assigned internally by service
                active:
                  type: boolean
                  description: the status of customer whether it is currently active (true) or not (false)
                address_line1:
                  type: string
                  description: address line 1 of the customer
                address_line2:
                  type: string
                  description: address line 2 of the customer
                age:
                  type: integer
                  description: age of the customer
                email:
                  type: string
                  description: email address of the customer
                first_name:
                  type: string
                  description: first name of the customer
                last_name:
                  type: string
                  description: last name of the customer
                gender:
                  type: string
                  description: gender of the customer
                phonenumber:
                  type: string
                  description: phone number of the customer
    """
    customers = []
    email = request.args.get('email')
    last_name = request.args.get('last-name')
    first_name = request.args.get('first-name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    address_line1 = request.args.get('address-line1')
    address_line2 = request.args.get('address-line2')
    phonenumber = request.args.get('phonenumber')
    active = request.args.get('active')
    print(active)
    if email:
        customers = Customer.find_by_email(redis, email)
    elif last_name:
        customers = Customer.find_by_last_name(redis, last_name)
    elif first_name:
        customers = Customer.find_by_first_name(redis, first_name)
    elif age:
        customers = Customer.find_by_age(redis, age)
    elif gender:
        customers = Customer.find_by_gender(redis, gender)
    elif address_line1:
        customers = Customer.find_by_address_line1(redis, address_line1)
    elif address_line2:
        customers = Customer.find_by_address_line2(redis, address_line2)
    elif phonenumber:
        customers = Customer.find_by_phonenumber(redis, phonenumber)
    elif active:
		customers = Customer.find_by_activity(redis, str(active).lower())
    else:
        customers = Customer.all(redis)

    results = [Customer.serialize(customer) for customer in customers]
    return make_response(jsonify(results), HTTP_200_OK)

######################################################################
# RETRIEVE A customer
######################################################################
@app.route('/customers/<int:id>', methods=['GET'])
def get_customers(id):
    customer = Customer.find(redis, id)
    if customer:
        message = customer.serialize()
        rc = HTTP_200_OK
    else:
        message = { 'error' : 'Customer with id: %s was not found' % str(id) }
        rc = HTTP_404_NOT_FOUND

    return make_response(jsonify(message), rc)

######################################################################
# ADD A NEW customer
######################################################################
@app.route('/customers', methods=['POST'])
def create_customers():
    id = 0
    payload = request.get_json()
    if Customer.validate(payload):
        customer = Customer(id, payload['first_name'], payload['last_name'],payload['gender'],payload['age'],payload['email'],payload['address_line1'],payload['address_line2'],payload['phonenumber'], True)
        customer.save(redis)
        id = customer.id
        cust = Customer.find(redis, id) # added so that the response body of POST matches that of the GET and we compare the results in the TDD in the same format as the json returned by Redis
        #message = customer.serialize()
        message = cust.serialize()
        rc = HTTP_201_CREATED
    else:
        message = { 'error' : 'Data is not valid' }
        rc = HTTP_400_BAD_REQUEST

    response = make_response(jsonify(message), rc)
    if rc == HTTP_201_CREATED:
        response.headers['Location'] = url_for('get_customers', id=id)
    return response

######################################################################
# UPDATE AN EXISTING customer
######################################################################
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customers(id):
    customer = Customer.find(redis, id)
    if customer:
        active = customer.active
        payload = request.get_json()
        if Customer.validate(payload):
            customer = Customer.from_dict(payload)
            customer.id = id				# so that the id in the URI is utilized
            customer.active = active		# restore the activity status
            customer.save(redis)
            message = customer.serialize()
            rc = HTTP_200_OK
        else:
            message = { 'error' : 'Customer data was not valid' }
            rc = HTTP_400_BAD_REQUEST
    else:
        message = { 'error' : 'Customer %s was not found' % id }
        rc = HTTP_404_NOT_FOUND

    return make_response(jsonify(message), rc)

######################################################################
# DELETE A customer
######################################################################
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customers(id):
    customer = Customer.find(redis, id)
    if customer:
        customer.delete(redis)
    return make_response('', HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def data_load(payload):
    customers = Customer(0, payload['first_name'], payload['last_name'],payload['gender'],payload['age'],payload['email'],payload['address_line1'],payload['address_line2'],payload['phonenumber'], True)
    customers.save(redis)

def data_reset():
    redis.flushall()

######################################################################
#  Redis Setup
######################################################################

def connect_to_redis(hostname, port, password):
    redis = Redis(host=hostname, port=port, password=password)
    try:
        redis.ping()
    except ConnectionError:
        redis = None
    return redis

def inititalize_redis():
    global redis
    redis = None
    # Get the crdentials from the Bluemix environment
    if 'VCAP_SERVICES' in os.environ:
        app.logger.info("Using VCAP_SERVICES...")
        VCAP_SERVICES = os.environ['VCAP_SERVICES']
        services = json.loads(VCAP_SERVICES)
        creds = services['rediscloud'][0]['credentials']
        app.logger.info("Conecting to Redis on host %s port %s" % (creds['hostname'], creds['port']))
        redis = connect_to_redis(creds['hostname'], creds['port'], creds['password'])
    else:
        app.logger.info("VCAP_SERVICES not found, checking localhost for Redis")
        redis = connect_to_redis('127.0.0.1', 6379, None)
        if not redis:
            app.logger.info("No Redis on localhost, using: redis")
            redis = connect_to_redis('redis', 6379, None)
    if not redis:
        # if you end up here, redis instance is down.
        app.logger.error('*** FATAL ERROR: Could not connect to the Redis Service')
        exit(1)

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    inititalize_redis()
    app.run(host='0.0.0.0', port=int(port), debug=debug)
