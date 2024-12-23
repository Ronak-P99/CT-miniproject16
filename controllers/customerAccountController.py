from models.schemas.customerAccountSchema import customer_account_schema, customer_accounts_schema
from services import customerAccountService
from marshmallow import ValidationError
from flask import jsonify, request

def save():
    # Post Request. /customers POST contain JSON
    try:
        # Validate and deserialize input
        customer_account_data = customer_account_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    customer_account_save = customerAccountService.save(customer_account_data)
    if customer_account_save is not None:
        return customer_account_schema.jsonify(customer_account_save), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":customer_account_data}), 400

def update(id):
    try:
        # Validate and deserialize input
        customer_account_data = customer_account_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    customer_account_save = customerAccountService.update(id, customer_account_data)
    if customer_account_save is not None:
        return customer_account_schema.jsonify(customer_account_save), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":customer_account_data}), 400

def delete(id):
    try:
        # Validate and deserialize input
        result = customerAccountService.delete(id)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    if result is not None:
        return jsonify({"message":result}), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":result}), 400

def find_by_id(id):
    customer = customerAccountService.find_by_id(id)
    return customer_account_schema.jsonify(customer), 200
    
def find_all():
    customer_accounts = customerAccountService.find_all()
    return customer_accounts_schema.jsonify(customer_accounts), 200

def login():
    customer = request.json
    user = customerAccountService.login_customer(customer['username'], customer['password'])
    if user:
        return jsonify(user), 200
    else:
        resp ={
            "status": "Error",
            "message":"User does not exist"
        }
        return jsonify(resp), 404