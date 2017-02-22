@app.route('/customers', methods=['GET'])
def list_customers():
    results = []
    gender = request.args.get('gender')
    if gender:
        results = [customer for customer in customers if customer['gender'] == gender]
    else:
        results = customers
    return make_response(jsonify(results), HTTP_200_OK)