from marshmallow import fields, validate
from schema import ma

class EmployeeSchema(ma.Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True, validate=validate.Length(min=1))
    position = fields.String(required=True, validate=validate.Length(min=1))

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)