
customers = [
    {
        'id': 1,
        'name': 'fido',
        'gender': 'male',
        'age': 23,
        'email': 'fido1@gmail.com',
        'address-line':'10420 Queens Blvd',
        'phonenumber' : 123456      
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

@app.route('/customers', methods=['POST'])
def create_customers():
    payload = request.get_json()
    if is_valid(payload):
        id = next_index()
        customer = {'id': id, 'name': payload['name'], 'gender': payload['gender'], 'age': payload['age'],'email':payload['email'], 'address-line': payload['address-line'], 'phonenumber': payload['phonenumber']}
        customers.append(customer)
        message = customer
        rc = HTTP_201_CREATED
    else:
        message = { 'error' : 'Data is not valid' }
        rc = HTTP_400_BAD_REQUEST

    return make_response(jsonify(message), rc)