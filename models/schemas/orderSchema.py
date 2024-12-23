from marshmallow import fields
from schema import ma

class OrderSchema(ma.Schema):
    id = fields.Integer(required=False)
    date = fields.Date(required=True)
    customer_id = fields.Integer(required=True)
    products = fields.Nested('ProductSchemaId', many=True)

class OrderSchemaCustomer(ma.Schema):
    id = fields.Integer(required=False)
    date = fields.Date(required=True)
    customer = fields.Nested('CustomerSchema')
    products = fields.Nested('ProductSchema', many=True)

order_schema_customer = OrderSchemaCustomer()


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)