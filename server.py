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

# Create Flask applifion
app = Flask(__name__)
app.config['LOGGING_LEVEL'] = logging.INFO

debug = (os.getenv('DEBUG', 'False') == 'True')
port = os.getenv('PORT', '5000')


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
# LIST ALL customers
######################################################################
@app.route('/customers', methods=['GET'])
def list_customers():
    customers = []
    email = request.args.get('email')
    last_name = request.args.get('last_name')
    first_name = request.args.get('first_name')
    age = request.args.get('age')
    address_line1 = request.args.get('address_line1')
    address_line2 = request.args.get('address_line2')
    phonenumber = request.args.get('phonenumber')
    if email:
        customers = Customer.find_by_email(redis, email)
    elif last_name:
        customers = Customer.find_by_last_name(redis, last_name)
    elif first_name:
        customers = Customer.find_by_first_name(redis, first_name)
    elif age:
        customers = Customer.find_by_age(redis, age)
    elif address_line1:
        customers = Customer.find_by_address_line1(redis, address_line1)
    elif address_line2:
        customers = Customer.find_by_address_line2(redis, address_line2)
    elif phonenumber:
        customers = Customer.find_by_phonenumber(redis, phonenumber)
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
        customer = Customer(id, payload['first_name'], payload['last_name'],payload['gender'],payload['age'],payload['email'],payload['address_line1'],payload['address_line2'],payload['phonenumber'])
        customer.save(redis)
        id = customer.id
        message = customer.serialize()
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
        payload = request.get_json()
        if Customer.validate(payload):
            customer = Customer.from_dict(payload)
            customer.id = id				# so that the id in the URI is utilized
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
    customers = customer(0, payload['first_name'], payload['last_name'],payload['gender'],payload['age'],payload['email'],payload['address_line1'],payload['address_line2'],payload['phonenumber'])
    customers.save(redis)

def data_reset():
    redis.flushall()


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
    print "Customer Service Starting..."
    inititalize_redis()
    app.run(host='0.0.0.0', port=int(port), debug=debug)
