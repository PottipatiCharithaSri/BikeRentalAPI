from marshmallow import Schema, fields

class BikeSchema(Schema):
    model = fields.Str(required=True)