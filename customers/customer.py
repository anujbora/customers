# Copyright 2016 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class Customer(object):
######################################################################
# Constructor to define all customer information
######################################################################
    def __init__(self, id, first_name, last_name, gender, age, email, address_line1, address_line2, phonenumber):
		self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.age = age
        self.email = email
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.phonenumber = phonenumber

######################################################################
# Saves the entire customer object data in the Redis database
######################################################################
    def save(self, redis):
        if self.id == 0:
            self.id = self.__next_index(redis)
        redis.hmset(self.id, self.serialize())

######################################################################
# Deletes the customer object from the Redis database
######################################################################
    def delete(self, redis):
        redis.delete(self.id)

######################################################################
# Get the next value of the index key stored in the Redis database
######################################################################
    def __next_index(self, redis):
        redis.incr('index')
        index = redis.get('index')
        return index

######################################################################
# Convert the object into a dictionary object
######################################################################
    def serialize(self):
        return self.__dict__

######################################################################
# Call the Customer constructor using the ID value in the payload
######################################################################
    @staticmethod
    def from_dict(data):
        # id is optional because it's a database key
        id = 0
        if data.has_key('id'):
            id = data['id']
        return Customer(id, data['first_name'], data['last_name'], data['gender'],
						data['age'], data['email'], data['address_line1'],
						data['address_line2'], data['phonenumber'])
						
######################################################################
# Validate the payload data with the required fields
######################################################################
    @staticmethod
    def validate(data):
        valid = False
        try:
			id = data['id']
			first_name = data['first_name']
			last_name = data['last_name']
			gender = data['gender']
			age = data['age']
			email = data['email']
			address_line1 = data['address_line1']
			address_line2 = data['address_line2']
			phonenumber = data['phonenumber']			
            valid = True
        except KeyError:
            valid = False
        except TypeError:
            valid = False
        return valid

		
######################################################################
# Return all Redis data that have key values different from 'index'
######################################################################
    @staticmethod
    def all(redis):
        # results = [Customer.from_dict(redis.hgetall(key)) for key in redis.keys() if key != 'index']
        results = []
        for key in redis.keys():
            if key != 'index':  # filter out our id index
                data = redis.hgetall(key)
                results.append(Customer.from_dict(data))
        return results

######################################################################
# Finds data from Redis based on ID and then returns a customer object
######################################################################
    @staticmethod
    def find(redis, id):
        if redis.exists(id):
            data = redis.hgetall(id)
            return Customer.from_dict(data)
        else:
            return None

	'''
    @staticmethod
    def find_by_category(redis, category):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if data['category'] == category:
                    results.append(Customer.from_dict(data))
        return results
	'''
