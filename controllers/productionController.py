from flask import request, jsonify
from models.schemas.productionSchema import production_schema, productions_schema
from services import productionService
from marshmallow import ValidationError
from caching import cache

def save():
    # Post Request. /productions POST contain JSON
    try:
        # Validate and deserialize input
        production_data = production_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    production_save = productionService.save(production_data)
    if production_save is not None:
        return production_schema.jsonify(production_save), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":production_data}), 400

def update(id):
    try:
        # Validate and deserialize input
        production_data = production_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    production_save = productionService.update(id, production_data)
    if production_save is not None:
        return production_schema.jsonify(production_save), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":production_data}), 400

def delete(id):
    try:
        # Validate and deserialize input
        result = productionService.delete(id)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    if result is not None:
        return jsonify({"message":result}), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":result}), 400

def find_by_id(id):
    production = productionService.find_by_id(id)
    return production_schema.jsonify(production), 200

@cache.cached(timeout=60)
def find_all():
    productions = productionService.find_all()
    return productions_schema.jsonify(productions), 200

def get_production_dates():
    result = productionService.get_production_dates()
    return jsonify(result), 200