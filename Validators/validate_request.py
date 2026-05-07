from functools import wraps

from flask import request, jsonify
from marshmallow import ValidationError

def validate(schema):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                schema().load(request.json)
            except ValidationError as err:
                return jsonify({"validation_error": err.messages}), 400
            return fn(*args, **kwargs)
        wrapper.__name__ = fn.__name__
        return wrapper
    return decorator
