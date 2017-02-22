@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customers(id):
    index = [i for i, customer in enumerate(customers) if customer['id'] == id]
    if len(index) > 0:
        del customers[index[0]]
    return make_response('', HTTP_204_NO_CONTENT)