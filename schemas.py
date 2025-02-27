"""Module to handle api schemas."""
from marshmallow import Schema, fields

class ItemSchema(Schema):
    """Items schema."""
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

class UpdateItemSchema(Schema):
    """Schema to update items."""
    name = fields.Str()
    price = fields.Float()

class StoreSchema(Schema):
    """Stores schema."""
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
