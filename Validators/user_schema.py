from marshmallow import Schema, fields, validate

class CreateUserSchema(Schema):
    name = fields.Str(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=1))