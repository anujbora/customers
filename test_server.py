# run with:
# python -m unittest discover
# nosetests --nologcapture

import logging
import unittest
import json
import server

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
class TestcustomerServer(unittest.TestCase):

    def setUp(self):
        server.app.debug = True
        server.app.logger.addHandler(logging.StreamHandler())
        server.app.logger.setLevel(logging.CRITICAL)

        self.app = server.app.test_client()
        server.customers = customers = [
            {
                'id': 1,
                'name': 'fido',
                'gender': 'male',
                'age': 23,
                'email': 'fido1@gmail.com',
                'address-line':'10420 Queens Blvd',
                'phonenumber' : 123456,      
            },
            {
                'id': 2,
                'name': 'shirley',
                'gender': 'female',
                'age': 22,
                'email': 'shirley2@gmail.com',
                'address-line':'8th street Mahaton',
                'phonenumber' : 234567   
            }
        ]
        server.current_customer_id = 2

    def test_index(self):
        resp = self.app.get('/')
        self.assertTrue ('customer Demo REST API Service' in resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )

    def test_get_customer_list(self):
        resp = self.app.get('/customers')
        #print 'resp_data: ' + resp.data
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )

    def test_get_customer(self):
        resp = self.app.get('/customers/2')
        #print 'resp_data: ' + resp.data
        self.assertTrue( resp.status_code == HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue (data['name'] == 'shirley')

    def test_create_customer(self):
        # save the current number of customers for later comparrison
        customer_count = self.get_customer_count()
        # add a new customer
        new_customer = {'name': 'sammy', 'gender': 'female', 'age': 18, 'email':'sammy@gmail.com', 'address-line':'lafayette street 404', 'phonenumber':'345678'}
        data = json.dumps(new_customer)
        resp = self.app.post('/customers', data=data, content_type='applifemaleion/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'sammy')
        # check that count has gone up and includes sammy
        resp = self.app.get('/customers')
        # print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(data) == customer_count + 1 )
        self.assertTrue( new_json in data )

    def test_update_customer(self):
        new_shirley = {'name': 'shirley','phonenumber' : 456789} #change her phonenumber
        data = json.dumps(new_shirley)
        resp = self.app.put('/customers/2', data=data, content_type='applifemaleion/json')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['phonenumber'] == '456789')

    def test_update_customer_with_no_name(self):
        new_customer = {'gender': 'male'}
        data = json.dumps(new_customer)
        resp = self.app.put('/customers/2', data=data, content_type='applifemaleion/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )

    def test_delete_customer(self):
        # save the current number of customers for later comparrison
        customer_count = self.get_customer_count()
        # delete a customer
        resp = self.app.delete('/customers/2', content_type='applifemaleion/json')
        self.assertTrue( resp.status_code == HTTP_204_NO_CONTENT )
        self.assertTrue( len(resp.data) == 0 )
        new_count = self.get_customer_count()
        self.assertTrue ( new_count == customer_count - 1)

    def test_create_customer_with_no_name(self):
        new_customer = {'gender': 'male'}
        data = json.dumps(new_customer)
        resp = self.app.post('/customers', data=data, content_type='applifemaleion/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )

    def test_create_customer_with_no_content_type(self):
        new_customer = {'gender': 'male'}
        data = json.dumps(new_customer)
        resp = self.app.post('/customers', data=data)
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )

    def test_get_nonexisting_customer(self):
        resp = self.app.get('/customers/5')
        self.assertTrue( resp.status_code == HTTP_404_NOT_FOUND )

    def test_query_customer_list(self):
        resp = self.app.get('/customers', query_string='gender=male')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertTrue(query_item['gender'] == 'male')


######################################################################
# Utility functions
######################################################################

    def get_customer_count(self):
        # save the current number of customers
        resp = self.app.get('/customers')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        # print 'resp_data: ' + resp.data
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
