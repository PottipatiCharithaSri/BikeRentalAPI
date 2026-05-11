from marshmallow import Schema, fields
from marshmallow import validate as ma_validate


class RentBikeSchema(Schema):
    bike_id = fields.Int(required=True)
    duration_value = fields.Int(
        required=True,
        validate=ma_validate.Range(min=1)
    )
    duration_unit = fields.Str(
        required=True,
        validate=ma_validate.OneOf(["HOURS", "DAYS", "WEEKS"])
    )


class ReturnRentalSchema(Schema):
    return_reason = fields.Str(
        required=True,
        validate=ma_validate.OneOf([
            "COMPLETED",
            "EARLY_RETURN",
            "BIKE_ISSUE",
            "CUSTOMER_REQUEST"
        ])
    )


class CancelRentalSchema(Schema):
    cancellation_reason = fields.Str(
        required=True,
        validate=ma_validate.OneOf([
            "CUSTOMER_CHANGED_MIND",
            "BIKE_UNAVAILABLE",
            "PAYMENT_FAILED",
            "ADMIN_CANCELLED"
        ])
    )