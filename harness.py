import os
from threading import Lock
from flask import Flask, Response, jsonify, request, json

import create_customers
import list_customers
import delete_customers
import update_customers
import get_customers

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def next_index():
    global current_pet_id
    with lock:
        current_pet_id += 1
    return current_pet_id

def reply(message, rc):
    response = Response(json.dumps(message))
    response.headers['Content-Type'] = 'application/json'
    response.status_code = rc
    return response

def is_valid(data):
    valid = False
    try:
        name = data['name']
        kind = data['kind']
        valid = True
    except KeyError as err:
        app.logger.error('Missing parameter error: %s', err)
    return valid


# Create Flask application
app = Flask(__name__)

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

# Lock for thread-safe counter increment
lock = Lock()


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    with open('customers.json') as json_file:
        data = json.load(json_file)
    # print(json.dumps(data,indent=2))
    # Pull options from environment
    debug = (os.getenv('DEBUG', 'False') == 'True')
    port = os.getenv('PORT', '5000')
    app.run(host='0.0.0.0', port=int(port), debug=debug)