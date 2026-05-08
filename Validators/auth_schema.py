from marshmallow import Schema, fields, validate, validates_schema, ValidationError
import re

class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, validate=validate.Length(min=6))

class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    name = fields.Str(required=True)
    age = fields.Int(required=True)  
    aadhar = fields.Str(required=False)
    licence = fields.Str(required=False)

    @validates_schema
    def validate_All(self, data, **kwargs):
        age = data.get("age")
        
        
        if not isinstance(age, int):
            raise ValidationError({"age": ["Enter your age in number"]})

        
        if age <= 18 or age >= 80:
            raise ValidationError({"age": ["You are not eligible"]})

        
        if not data.get("aadhar") and not data.get("licence"):
            raise ValidationError({
                "identity": ["Either Aadhaar or Licence is required for registration"]
            })

        
        if data.get("aadhar"):
            if not re.match(r"^[2-9][0-9]{11}$", data["aadhar"]):
                raise ValidationError({
                    "aadhar": [
                        "Invalid Aadhaar number. Must be 12 digits and not start with 0 or 1"
                    ]
                })
                
        
        if data.get("licence"):
            licence_pattern = r"^[A-Z]{2}[0-9]{2,4}[0-9]{4}[0-9]{7}$"
            if not re.match(licence_pattern, data["licence"]):
                raise ValidationError({
                    "licence": [
                        "Invalid licence number. Example valid format: KA0120190001234"
                    ]
                })
