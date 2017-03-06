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
    def find_by_gender(redis, gender):
        results = []
        for key in redis.keys():
            if key != 'index':  # filer out our id index
                data = redis.hgetall(key)
                if data['gender'] == gender:
                    results.append(Customer.from_dict(data))
        return results
