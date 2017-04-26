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

        server.data_load({"first_name": "Ronaldinho", "last_name": "Gaucho", "gender": "M",
        "age": "40", "email" : "r@g.br", "address_line1": "Barcelona",
        "address_line2": "Spain", "phonenumber": "999"})

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
        self.assertTrue ('Andrea' in resp.data)
        self.assertTrue ('Theirry' in resp.data)
        data = json.loads(resp.data)
        self.assertEqual( len(data), 2 )

    def test_get_customer_list_by_email(self):
        resp = self.app.get('/customers?email=a@p.com')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 1 )
        self.assertTrue('Andrea' in resp.data)

    def test_get_customer_list_by_name(self):
        resp = self.app.get('/customers?first-name=Andrea')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 1 )
        self.assertTrue('Andrea' in resp.data)
        resp = self.app.get('/customers?last-name=Pirlo')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 1 )
        self.assertTrue('Andrea' in resp.data)
        resp = self.app.get('/customers?first-name=Andrea&last-name=Pirlo')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 1 )
        self.assertTrue('Andrea' in resp.data)

    def test_create_customer(self):

         # save the current number of customers for later comparrison
         customer_count = self.get_customer_count()
         # add a new customer
         new_customer =  {"first_name": "Lionel", "last_name": "Messi", "gender": "M",
        "age": "29", "email" : "messi@barca.com", "address_line1": "Camp Nou",
        "address_line2": "Barcelona", "phonenumber": "666"}
         data = json.dumps(new_customer)
         resp = self.app.post('/customers', data=data, content_type='application/json')
         self.assertEqual( resp.status_code, status.HTTP_201_CREATED )
         # Make sure location header is set
         location = resp.headers.get('Location', None)
         self.assertTrue( location != None)
         # Check the data is correct
         new_json = json.loads(resp.data)
         self.assertEqual (new_json['first_name'], 'Lionel')
         # check that count has gone up and includes Lionel
         resp = self.app.get('/customers')
         # print 'resp_data(2): ' + resp.data
         data = json.loads(resp.data)
         self.assertEqual( resp.status_code, status.HTTP_200_OK )
         self.assertEqual( len(data), customer_count + 1 )
         self.assertIn(new_json,data)
         # checking the error response when adding a faulty customer
         faulty_customer = {"fname":"Dinosaur"}
         data = json.dumps(faulty_customer)
         resp = self.app.post('/customers', data=data, content_type='application/json')
         self.assertEqual( resp.status_code, status.HTTP_400_BAD_REQUEST )
         new_faulty_json = json.loads(resp.data)
         # make sure the correct error message is put out
         self.assertEqual (new_faulty_json['error'], 'Data is not valid')

    def test_get_customer_list_by_age(self):
        resp = self.app.get('/customers?age=40')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 1 )
        self.assertTrue('Ronaldinho' in resp.data)

    def test_get_customer_list_by_gender(self):
        resp = self.app.get('/customers?gender=M')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 3 )
        self.assertTrue('Ronaldinho' in resp.data)
        resp = self.app.get('/customers?gender=F')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 0 )

    def test_get_customer_list_by_address(self):
        resp = self.app.get('/customers?address-line1=London')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 1 )
        self.assertTrue('Henry' in resp.data)
        resp = self.app.get('/customers?address-line2=Italy')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 1 )
        self.assertTrue('Pirlo' in resp.data)

    def test_get_customer_list_by_phone(self):
        resp = self.app.get('/customers?phonenumber=123')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 1 )
        self.assertTrue('Andrea' in resp.data)
        resp = self.app.get('/customers?phonenumber=321')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 0 )

    def test_get_customer_list_by_activity(self):
        resp = self.app.get('/customers?active=True')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 3 )
        self.assertTrue('Andrea' in resp.data)
        resp = self.app.get('/customers?active=False')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual( len(data), 0 )

    def test_deactivate_valid_customer(self):
        resp = self.app.put('/customers/deactivate/1')
        self.assertEqual( resp.status_code, HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual (data['first_name'], 'Andrea')
        self.assertEqual (data['active'], False)

    def test_deactivate_invalid_customer(self):
        resp = self.app.put('/customers/deactivate/99')
        self.assertEqual( resp.status_code, HTTP_404_NOT_FOUND )
        data = json.loads(resp.data)
        self.assertTrue('Customer 99 was not found' in resp.data)

    def test_activate_valid_customer(self):
        resp = self.app.put('/customers/deactivate/1')
        data = json.loads(resp.data)
        self.assertEqual (data['active'], False)
        resp = self.app.put('/customers/activate/1')
        self.assertEqual( resp.status_code, HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual (data['first_name'], 'Andrea')
        self.assertEqual (data['active'], True)

    def test_activate_invalid_customer(self):
        resp = self.app.put('/customers/activate/99')
        self.assertEqual( resp.status_code, HTTP_404_NOT_FOUND )
        data = json.loads(resp.data)
        self.assertTrue('Customer 99 was not found' in resp.data)

    def test_update_valid_customer(self):
        updated_customer = {"first_name": "Ronaldinho", "last_name": "Gaucho", "gender": "M",
        "age": "40", "email" : "r@g.br", "address_line1": "PSG",
        "address_line2": "France", "phonenumber": "999"}
        data = json.dumps(updated_customer)
        resp = self.app.put('/customers/1', data=data, content_type='application/json')
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue("PSG" in data['address_line1'])
        self.assertTrue("France" in data['address_line2'])

    def test_update_invalid_customer(self):
        updated_customer = {"first_name": "Ronaldinho", "last_name": "Gaucho", "gender": "M",
        "age": "40", "email" : "r@g.br", "address_line1": "PSG",
        "address_line2": "France", "phonenumber": "999"}
        data = json.dumps(updated_customer)
        resp = self.app.put('/customers/99', data=data, content_type='application/json')
        self.assertEqual( resp.status_code, status.HTTP_404_NOT_FOUND )
        data = json.loads(resp.data)
        self.assertTrue("Customer 99 was not found" in data['error'])


######################################################################
# Utility functions
######################################################################

    def get_customer_count(self):
         # save the current number of customers
         resp = self.app.get('/customers')
         self.assertEqual( resp.status_code, status.HTTP_200_OK )
         data = json.loads(resp.data)
         return len(data)

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
