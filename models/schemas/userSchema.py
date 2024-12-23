from marshmallow import fields
from schema import ma

class UserSchema(ma.Schema):
    id = fields.Integer(required=False)
    username = fields.String(required=True)
    password = fields.String(required=True)

user_schema = UserSchema()
user_schema = UserSchema(many=True)

