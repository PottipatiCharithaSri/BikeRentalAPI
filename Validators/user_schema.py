from marshmallow import Schema, fields, validate

class CreateUserSchema(Schema):
    name = fields.Str(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=1))


class UpdateUserSchema(Schema):
    name = fields.Str(
        required=False,
        validate=validate.Length(min=2)
    )
    age = fields.Int(
        required=False,
        validate=validate.Range(min=1, max=120)
    )
