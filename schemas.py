from marshmallow import Schema, fields

class PlainUserSchema(Schema):
    id = fields.Str(dump_only=True) # add only when returning data from api
    name = fields.Str(required=True)

class PlainUploadedFileSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class UserUpdateSchema(Schema):
    name = fields.Str(required=True)


class UploadedFileSchema(Schema):
    user_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)

class UserSchema(PlainUserSchema):
    uploaded_files = fields.List(fields.Nested(PlainUploadedFileSchema()), dump_only=True)

