from marshmallow import Schema, fields

class StoreSchema(Schema):
    id = fields.Str(dump_only=True) # add only when returning data from api
    name = fields.Str(required=True)

class StoreUpdateSchema(Schema):
    name = fields.Str(required=True)

