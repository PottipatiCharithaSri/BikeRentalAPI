from marshmallow import Schema, fields, validate

class CreateUserSchema(Schema):
    name = fields.Str(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=1))



class UpdateUserSchema(Schema):
    username = fields.Str(
        required=False,
        validate=validate.Length(min=3)
    )
    password = fields.Str(
        required=False,
        validate=validate.Length(min=6)
    )

