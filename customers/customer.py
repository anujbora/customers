class Customer(object):

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
        self.active = True					#By default, any new customer created is marked as Active

    def save(self, redis):
        if self.id == 0:
            self.id = self.__next_index(redis)
        redis.hmset(self.id, self.serialize())

    def delete(self, redis):
        redis.delete(self.id)

    def __next_index(self, redis):
        redis.incr('index')
        index = redis.get('index')
        return index

    def serialize(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        # id is optional because it's a database key
        id = 0
        if data.has_key('id'):
            id = data['id']
        return Customer(id, data['first_name'], data['last_name'],data['gender'],data['age'],data['email'],data['address_line1'],data['address_line2'],data['phonenumber'])

    @staticmethod
    def validate(data):
        valid = False
        try:
            first_name = data['first_name']
            gender = data['gender']
            last_name = data['last_name']
            age = data['age']
            email = data['email']
            address_line1 = data['address_line1']
            address_line2 = data['address_line2']
            phonenumber = data['phonenumber']
            active = data['active']
            valid = True
        except KeyError:
            valid = False
        except TypeError:
            valid = False
        return valid

    @staticmethod
    def all(redis):
        # results = [Customer.from_dict(redis.hgetall(key)) for key in redis.keys() if key != 'index']
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                results.append(Customer.from_dict(data))
        return results

    @staticmethod
    def find(redis, id):
        if redis.exists(id):
            data = redis.hgetall(id)
            return Customer.from_dict(data)
        else:
            return None

    @staticmethod
    def find_by_email(redis, email):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if data['email'] == email:
                    results.append(Customer.from_dict(data))
        return results

    @staticmethod
    def find_by_first_name(redis, first_name):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if data['first_name'] == first_name:
                    results.append(Customer.from_dict(data))
        return results

    @staticmethod
    def find_by_gender(redis, gender):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if data['gender'] == gender:
                    results.append(Customer.from_dict(data))
        return results

    @staticmethod
    def find_by_age(redis, age):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if data['age'] == age:
                    results.append(Customer.from_dict(data))
        return results

    @staticmethod
    def find_by_phonenumber(redis, phonenumber):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if data['phonenumber'] == phonenumber:
                    results.append(Customer.from_dict(data))
        return results

    @staticmethod
    def find_by_activity(redis, active):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if data['active'] == active:
                    results.append(Customer.from_dict(data))
        return results
		
    @staticmethod
    def find_by_last_name(redis, last_name):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if data['last_name'] == last_name:
                    results.append(Customer.from_dict(data))
        return results

		
######################################################################
# SEARCH if keyword is part of the last_name
######################################################################	
    @staticmethod
    def search_in_last_name(redis, last_name):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if last_name in data['last_name']:
                    results.append(Customer.from_dict(data))
        return results
		
######################################################################
# SEARCH if keyword is part of the first_name
######################################################################	
    @staticmethod
    def search_in_first_name(redis, first_name):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if first_name in data['first_name']:
                    results.append(Customer.from_dict(data))
        return results

######################################################################
# SEARCH if keyword is part of the address_line1
######################################################################	
    @staticmethod
    def search_in_address_line1(redis, address_line1):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if address_line1 in data['address_line1']:
                    results.append(Customer.from_dict(data))
        return results

######################################################################
# SEARCH if keyword is part of the address_line2
######################################################################	
    @staticmethod
    def search_in_address_line2(redis, address_line2):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if address_line2 in data['address_line2']:
                    results.append(Customer.from_dict(data))
        return results

######################################################################
# SEARCH if keyword is part of the email
######################################################################	
    @staticmethod
    def search_in_email(redis, email):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if email in data['email']:
                    results.append(Customer.from_dict(data))
        return results

######################################################################
# SEARCH if keyword is part of the phonenumber
######################################################################	
    @staticmethod
    def search_in_phonenumber(redis, phonenumber):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if phonenumber in data['phonenumber']:
                    results.append(Customer.from_dict(data))
        return results

######################################################################
# SEARCH if keyword is part of the age
######################################################################	
    @staticmethod
    def search_in_age(redis, age):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if age in data['age']:
                    results.append(Customer.from_dict(data))
        return results