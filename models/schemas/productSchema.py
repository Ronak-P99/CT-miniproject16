from marshmallow import fields, validate
from schema import ma

class ProductSchema(ma.Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    order_id = fields.Integer(required=True)
    quantity_ordered = fields.Integer(required=True)

class ProductSchemaId(ma.Schema):
    id = fields.Integer(required=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

