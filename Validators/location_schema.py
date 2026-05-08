from marshmallow import Schema, fields, validate

class LocationSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2)
    )
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
