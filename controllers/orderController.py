from flask import request, jsonify
from models.schemas.orderSchema import order_schema, orders_schema, order_schema_customer
from services import orderService
from marshmallow import ValidationError
from caching import cache

def save():
    # Post Request. /orders POST contain JSON
    try:
        # Validate and deserialize input
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    try:
        order_save = orderService.save(order_data)
        return order_schema.jsonify(order_save), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

def update(id):
    try:
        # Validate and deserialize input
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    order_save = orderService.update(id, order_data)
    if order_save is not None:
        return order_schema.jsonify(order_save), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":order_data}), 400

def delete(id):
    try:
        # Validate and deserialize input
        result = orderService.delete(id)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    if result is not None:
        return jsonify({"message":result}), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":result}), 400

def find_by_id(id):
    order = orderService.find_by_id(id)
    return order_schema.jsonify(order), 200

def find_all_pagination():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return orders_schema.jsonify(orderService.find_all_pagination(page=page, per_page=per_page)), 200

# @cache.cached(timeout=60)
def find_all():
    orders = orderService.find_all()
    return orders_schema.jsonify(orders), 200