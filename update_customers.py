@app.route('/customers/<int:id>', methods=['PUT'])
def update_customers(id):
    index = [i for i, customer in enumerate(customers) if customer['id'] == id]
    if len(index) > 0:
        payload = request.get_json()
        if is_valid(payload):
            customers[index[0]] = {'id': id, 'first-name': payload['first-name'], 'last-name': payload['last-name'], 'gender': payload['gender'], 'age': payload['age'],'email':payload['email'], 'address-line1': payload['address-line1'], 'address-line2': payload['address-line2'],'phonenumber': payload['phonenumber']}
            message = customers[index[0]]
            rc = HTTP_200_OK
        else:
            message = { 'error' : 'customer data was not valid' }
            rc = HTTP_400_BAD_REQUEST
    else:
        message = { 'error' : 'customer %s was not found' % id }
        rc = HTTP_404_NOT_FOUND

    return make_response(jsonify(message), rc)