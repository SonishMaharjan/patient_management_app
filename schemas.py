from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.Str(dump_only=True) # add only when returning data from api
    name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

    
class UserSchema(PlainUserSchema):
    uploaded_files = fields.List(fields.Nested(lambda: PlainUploadedFileSchema()), dump_only=True)


class UserUpdateSchema(Schema):
    name = fields.Str(required=True)
    
    
class PlainUploadedFileSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    

class UploadedFileSchema(PlainUploadedFileSchema):
    user_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    
class UploadedFileUpdateSchema(Schema):
    name = fields.Str(required=True)
    user_id = fields.Int()
