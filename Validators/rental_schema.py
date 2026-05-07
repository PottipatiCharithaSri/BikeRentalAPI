from marshmallow import Schema, fields

class RentBikeSchema(Schema):
    user_id = fields.Int(required=True)
    bike_id = fields.Int(required=True)

class ReturnBikeSchema(Schema):
    bike_id = fields.Int(required=True)