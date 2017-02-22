@app.route('/customers', methods=['GET'])
def list_customers():
    results = []
    searchlist = ['gender','age']
    for key in searchlist:
        _key = request.args.get(key)
        if _key:
            results = [customer for customer in customers if customer[key] == _key]
        else:
            results = customers
    return make_response(jsonify(results), HTTP_200_OK)