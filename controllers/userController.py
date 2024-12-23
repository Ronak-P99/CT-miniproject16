from models.schemas.userSchema import user_schema
from services import userService
from flask import jsonify, request

def find_all():
    user_accounts = userService.find_all()
    return user_schema.jsonify(user_accounts), 200

def login():
    users = request.json
    user = userService.login_customer(users['username'], users['password'])
    if user:
        return jsonify(user), 200
    else:
        resp ={
            "status": "Error",
            "message":"User does not exist"
        }
        return jsonify(resp), 404