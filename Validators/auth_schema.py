from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, validate=validate.Length(min=6))


class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    name = fields.Str(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=1))
    admin_key = fields.Str(required=False)