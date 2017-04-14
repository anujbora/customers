# Test cases can be run with either of the following:
# python -m unittest discover
# nosetests -v --rednose --nologcapture

import unittest
import logging
import json
from flask_api import status    # HTTP Status Codes
import server
from customers import Customer

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomerServer(unittest.TestCase):

    def setUp(self):
        server.app.debug = True
        server.app.logger.addHandler(logging.StreamHandler())
        server.app.logger.setLevel(logging.CRITICAL)

        self.app = server.app.test_client()
        server.inititalize_redis()
        server.data_reset()
        #server.data_load({"name": "fido", "category": "dog"})

        server.data_load({"first_name": "Andrea", "last_name": "Pirlo", "gender": "M",
        "age": "35", "email" : "a@p.com", "address_line1": "Milan",
        "address_line2": "Italy", "phonenumber": "123"})

        server.data_load({"first_name": "Theirry", "last_name": "Henry", "gender": "M",
        "age": "30", "email" : "t@h.com", "address_line1": "London",
        "address_line2": "England", "phonenumber": "444"})

        #server.data_load({"name": "kitty", "category": "cat"})

    def test_get_customer_list(self):
        resp = self.app.get('/customers')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue( len(data) > 0 )

    def test_index(self):
        resp = self.app.get('/')
        self.assertEqual( resp.status_code, HTTP_200_OK )
        self.assertTrue ('Customer REST API Service' in resp.data)

    def test_get_customer(self):
        resp = self.app.get('/customers/1')
        #print 'resp_data: ' + resp.data
        self.assertEqual( resp.status_code, HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual (data['first_name'], 'Andrea')

    def test_get_customer_not_found(self):
        resp = self.app.get('/customers/0')
        self.assertEqual( resp.status_code, HTTP_404_NOT_FOUND )

    def test_delete_customer(self):
        # save the current number of customers for later comparison
        customer_count = self.get_customer_count()
        # delete a customer
        resp = self.app.delete('/customers/2', content_type='application/json')
        self.assertEqual( resp.status_code, HTTP_204_NO_CONTENT )
        self.assertEqual( len(resp.data), 0 )
        new_count = self.get_customer_count()
        self.assertEqual( new_count, customer_count - 1)

    def test_repeated_delete_customer(self):
        # save the current number of customers for later comparison
        customer_count = self.get_customer_count()
        # delete a customer
        resp = self.app.delete('/customers/2', content_type='application/json')
        self.assertEqual( resp.status_code, HTTP_204_NO_CONTENT )
        self.assertEqual( len(resp.data), 0 )
        new_count = self.get_customer_count()
        self.assertEqual( new_count, customer_count - 1)

        #delete same customer again
        resp = self.app.delete('/customers/2', content_type='application/json')
        self.assertEqual( resp.status_code, HTTP_204_NO_CONTENT )
        self.assertEqual( len(resp.data), 0 )
        new_count = self.get_customer_count()
        self.assertEqual( new_count, customer_count - 1)

    def test_update_customer_not_found(self):
        new_customer = {"first_name": "Andrea", "last_name": "Pirlo", "gender": "M",
        "age": "35", "email" : "a@p.com", "address_line1": "Milan",
        "address_line2": "Italy", "phonenumber": "123456789"}
        data = json.dumps(new_customer)
        resp = self.app.put('/customers/0', data=data, content_type='application/json')
        self.assertEquals( resp.status_code, HTTP_404_NOT_FOUND )

    def test_search_by_keyword(self):
        resp = self.app.get('/customers/search-keyword/com', content_type='application/json')
        self.assertEqual( resp.status_code, HTTP_200_OK )
        #self.assertEqual( len(resp.data), 2 )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 2 )
        self.assertEqual (data[0]['first_name'], 'Andrea')
        self.assertEqual (data[1]['first_name'], 'Theirry')


######################################################################
# Utility functions
######################################################################

    def get_customer_count(self):
        # save the current number of pets
        resp = self.app.get('/customers')
        self.assertEqual( resp.status_code, HTTP_200_OK )
        data = json.loads(resp.data)
        return len(data)
######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
