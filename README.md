# Customer REST API Service for E-Commerce website
This repository is part of lab for the *NYU DevOps* class for Spring 2017, [CSCI-GA.3033-013](http://cs.nyu.edu/courses/spring17/CSCI-GA.3033-013/)

This RESTful customer API contains the basic CRUD operation and some actions as follow:

## GET

**LIST all customers data**

Go to https://nyu-customers-service-alpha.mybluemix.net/customers in browser to check out all customers information. The data format is like:

```bash
    {
        active: "True",
        address_line1: "Hakunamatata",
        address_line2: "Hawaii",
        age: "40",
        email: "ajolie@jolie.com",
        first_name: "Angelina",
        gender: "F",
        id: "5",
        last_name: "Jolie",
        phonenumber: ""
    }
```

**Query the customer information by attribute**

Go to https://nyu-customers-service-alpha.mybluemix.net/customers?attribute=abc in browser and substitute 'attribute' into the attribute you want to search and subsitute 'abc' into the content you want to find.

For instance, enter https://nyu-customers-service-alpha.mybluemix.net/customers?gender=F in browser and get results:

    [
        {
            active: "True",
            address_line1: "Hakunamatata",
            address_line2: "Hawaii",
            age: "40",
            email: "ajolie@jolie.com",
            first_name: "Angelina",
            gender: "F",
            id: "5",
            last_name: "Jolie",
            phonenumber: ""
        },
        {
            active: "True",
            address_line1: "Hollywood",
            address_line2: "Los Angeles",
            age: "26",
            email: "kstew@stew.com",
            first_name: "Kristen",
            gender: "F",
            id: "4",
            last_name: "Stewart",
            phonenumber: ""
        }
    ]

**Retrieves a customer from the DB using an ID**

Go to https://nyu-customers-service-alpha.mybluemix.net/customers/{id} in browser and substitute '{id}' into the id number of customer.

For instance, enter https://nyu-customers-service-alpha.mybluemix.net/customers/5 to check the customer whose id is 5

**Retrieves all customers which contain the searched keyword**

This function is used to search all customers whose information contains the keyword whether the keyword is complete or not.
**Attention** This search is an case sensitive search.
Go to https://nyu-customers-service-alpha.mybluemix.net/customers/search-keyword/{content} in browser and substitue the '{content}' into any content to be searched.

For instance, enter https://nyu-customers-service-alpha.mybluemix.net/customers/search-keyword/wood to search customers with wood and get results:

```bash
  [
    {
        active: "True",
        address_line1: "Pacific Drive",
        address_line2: "USA",
        age: "43",
        email: "woodywoods@woods.com",
        first_name: "Tiger",
        gender: "M",
        id: "6",
        last_name: "Woods",
        phonenumber: ""
    },
    {
        active: "True",
        address_line1: "Hollywood",
        address_line2: "Los Angeles",
        age: "26",
        email: "kstew@stew.com",
        first_name: "Kristen",
        gender: "F",
        id: "4",
        last_name: "Stewart",
        phonenumber: ""
    },
    {
        active: "True",
        address_line1: "Hollywood Boulevard",
        address_line2: "",
        age: "51",
        email: "jstatam@gmail.com",
        first_name: "Jason",
        gender: "M",
        id: "2",
        last_name: "Statham",
        phonenumber: ""
    }
]
```

## PUT

**Activate the customer**

Sometimes a customer may be autherized to be the user of the website so that we design an action to activate the customer.
Do PUT in https://nyu-customers-service-alpha.mybluemix.net/customers/activate/{id} in RESTful client and substitute the '{id}' into the customer id. The the status of active of that customer will be True after the action.

For instance: 
```bash
    {
        active: "True",
        address_line1: "Hollywood Boulevard",
        address_line2: "",
        age: "51",
        email: "jstatam@gmail.com",
        first_name: "Jason",
        gender: "M",
        id: "2",
        last_name: "Statham",
        phonenumber: ""
    }
```

**Deactivate the customer**

Sometimes a customer may be unautherized to be the user of the website so that we design an action to deactivate the customer.
Do PUT  https://nyu-customers-service-alpha.mybluemix.net/customers/deactivate/{id} in RESTful client and substitute the '{id}' into the customer id. The the status of active of that customer will be False after the action.

For instance: 
```bash
    {
        active: "False",
        address_line1: "Hollywood Boulevard",
        address_line2: "",
        age: "51",
        email: "jstatam@gmail.com",
        first_name: "Jason",
        gender: "M",
        id: "2",
        last_name: "Statham",
        phonenumber: ""
    }
```

**Updates a customer using an ID**

Do PUT  https://nyu-customers-service-alpha.mybluemix.net/customers/{id} in RESTful client and substitute the '{id}' into the customer id. Then the content of that customer will be updated.

## DELETE

Do DELETE https://nyu-customers-service-alpha.mybluemix.net/customers/{id} in RESTful client and substitute the '{id}' into the customer id. Then the content of that customer will be deleted.

## POST

Do POST https://nyu-customers-service-alpha.mybluemix.net/customers in RESTful client Then the content of that customer will be added.




**README.md** - this readme.

**manifest.yml** - Controls how the app will be deployed in Bluemix and specifies memory and other services like Redis that are needed to be bound to it.

**server.py** - the python application script. This is implemented as a simple [Flask](http://flask.pocoo.org/) application. The routes are defined in the application using the @app.route() calls. 

This is the port given to your application so that http requests can be routed to it. If the property is not defined then it falls back to port 5000 allowing you to run this sample application locally.
