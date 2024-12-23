from flask import request, jsonify
from models.schemas.employeeSchema import employee_schema, employees_schema
from services import employeeService
from marshmallow import ValidationError
from caching import cache


def save():
    # Post Request. /employees POST contain JSON
    try:
        # Validate and deserialize input
        employee_data = employee_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    employee_save = employeeService.save(employee_data)
    if employee_save is not None:
        return employee_schema.jsonify(employee_save), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":employee_data}), 400

def update(id):
    try:
        # Validate and deserialize input
        employee_data = employee_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    employee_save = employeeService.update(id, employee_data)
    if employee_save is not None:
        return employee_schema.jsonify(employee_save), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":employee_data}), 400

def delete(id):
    try:
        # Validate and deserialize input
        result = employeeService.delete(id)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    if result is not None:
        return jsonify({"message":result}), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":result}), 400

def find_by_id(id):
    employee = employeeService.find_by_id(id)
    return employee_schema.jsonify(employee), 200

@cache.cached(timeout=60)
def find_all():
    employees = employeeService.find_all()
    return employees_schema.jsonify(employees), 200

def get_production():
    result = employeeService.get_production()
    return jsonify(result), 200




