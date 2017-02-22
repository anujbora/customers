
customers = [
    {
        'id': 1,
        'first-name': 'fido',
        'last-name': 'jack',
        'gender': 'M',
        'age': 23,
        'email': 'fido1@gmail.com',
        'address-line1':'10420 Queens Blvd',
        'address-line2':'16-V'
        'phonenumber' : 123456      
    },
    {
        'id': 2,
        'first-name': 'shirley',
        'last-name':'yang',
        'gender': 'F',
        'age': 22,
        'email': 'shirley2@gmail.com',
        'address-line1':'8th street Mahaton',
        'address-line2':'404 room',
        'phonenumber' : 234567   
    }
]

@app.route('/customers', methods=['POST'])
def create_customers():
    payload = request.get_json()
    if is_valid(payload):
        id = next_index()
        customer = {'id': id, 'first-name': payload['first-name'],'last-name': payload['last-name'],'gender': payload['gender'], 'age': payload['age'],'email':payload['email'], 'address-line1': payload['address-line1'], 'address-line2':payload['address-line2'], 'phonenumber': payload['phonenumber']}
        customers.append(customer)
        message = customer
        rc = HTTP_201_CREATED
    else:
        message = { 'error' : 'Data is not valid' }
        rc = HTTP_400_BAD_REQUEST

    return make_response(jsonify(message), rc)