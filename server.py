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
from threading import Lock
from flask import Flask, Response, jsonify, request, make_response, json, url_for

# Create Flask applifion
app = Flask(__name__)
app.config['LOGGING_LEVEL'] = logging.INFO

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

# Lock for thread-safe counter increment
lock = Lock()

# dummy data for testing
current_customer_id = 2
customers = [
    {
        'id': 1,
        'first_name': 'fido',
        'last_name': 'jack',
        'gender': 'M',
        'age': 23,
        'email': 'fido1@gmail.com',
        'address_line1':'10420 Queens Blvd',
        'address_line2':'16-V',
        'phonenumber':123456      
    },
    {
        'id': 2,
        'first_name': 'shirley',
        'last_name':'yang',
        'gender': 'F',
        'age': 22,
        'email': 'shirley2@gmail.com',
        'address_line1':'8th street Mahaton',
        'address_line2':'404 room',
        'phonenumber':234567   
    }
]

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    customers_url = request.base_url + "customers"
    return make_response(jsonify(name='customer Demo REST API Service',
                   version='1.0',
                   url=customers_url
                   ), HTTP_200_OK)

######################################################################
# LIST ALL customerS
######################################################################
@app.route('/customers', methods=['GET'])
def list_customers():
    results = []
    gender = request.args.get('gender')
    if gender:
        results = [customer for customer in customers if customer['gender'] == gender]
    else:
        results = customers

    return make_response(jsonify(results), HTTP_200_OK)

######################################################################
# RETRIEVE A customer
######################################################################
@app.route('/customers/<int:id>', methods=['GET'])
def get_customers(id):
    index = [i for i, customer in enumerate(customers) if customer['id'] == id]
    if len(index) > 0:
        message = customers[index[0]]
        rc = HTTP_200_OK
    else:
        message = { 'error' : 'customer with id: %s was not found' % str(id) }
        rc = HTTP_404_NOT_FOUND

    return make_response(jsonify(message), rc)

######################################################################
# ADD A NEW customer
######################################################################
@app.route('/customers', methods=['POST'])
def create_customers():
    payload = request.get_json()
    if is_valid(payload):
        id = next_index()
        customer = {'id': id, 'first_name': payload['first_name'],'last_name': payload['last_name'],'gender': payload['gender'], 'age': payload['age'],'email':payload['email'], 'address_line1': payload['address_line1'], 'address_line2':payload['address_line2'], 'phonenumber': payload['phonenumber']}
        customers.append(customer)
        message = customer
        rc = HTTP_201_CREATED
    else:
        message = { 'error' : 'Data is not valid' }
        rc = HTTP_400_BAD_REQUEST

    response = make_response(jsonify(message), rc)
    if rc == HTTP_201_CREATED:
        response.headers['Lofion'] = url_for('get_customers', id=id)
    return response

######################################################################
# UPDATE AN EXISTING customer
######################################################################
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customers(id):
    index = [i for i, customer in enumerate(customers) if customer['id'] == id]
    if len(index) > 0:
        payload = request.get_json()
        if is_valid(payload):
            customers[index[0]] = {'id': id, 'first_name': payload['first_name'], 'last_name': payload['last_name'], 'gender': payload['gender'], 'age': payload['age'],'email':payload['email'], 'address_line1': payload['address_line1'], 'address_line2': payload['address_line2'],'phonenumber': payload['phonenumber']}
            message = customers[index[0]]
            rc = HTTP_200_OK
        else:
            message = { 'error' : 'customer data was not valid' }
            rc = HTTP_400_BAD_REQUEST
    else:
        message = { 'error' : 'customer %s was not found' % id }
        rc = HTTP_404_NOT_FOUND

    return make_response(jsonify(message), rc)

######################################################################
# DELETE A customer
######################################################################
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customers(id):
    index = [i for i, customer in enumerate(customers) if customer['id'] == id]
    if len(index) > 0:
        del customers[index[0]]
    return make_response('', HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def next_index():
    global current_customer_id
    with lock:
        current_customer_id += 1
    return current_customer_id

def is_valid(data):
    valid = False
    try:
        first_name = data['first_name']
        last_name = data['last_name']
        gender = data['gender']
        age = data['age']
        email = data['email']
        address_line1 = data['address_line1']
        address_line2 = data['address_line2']
        phonenumber = data['phonenumber']
        valid = True
    except KeyError as err:
        app.logger.warn('Missing parameter error: %s', err)
    except TypeError as err:
        app.logger.warn('Invalid Content Type error: %s', err)

    return valid

@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        handler = logging.StreamHandler()
        handler.setLevel(app.config['LOGGING_LEVEL'])
        # formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
        #'%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    # Pull options from environment
    debug = (os.getenv('DEBUG', 'False') == 'True')
    port = os.getenv('PORT', '5000')
    app.run(host='0.0.0.0', port=int(port), debug=debug)
