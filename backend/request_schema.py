from backend import ma
from marshmallow import fields

class ProductCreateSchema(ma.Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True, error_messages=)