from marshmallow import Schema, fields, post_load
from models.user import UserModel


class Archived(Schema):
    value = fields.Str()
    at = fields.Str()


class UserSchema(Schema):
    _id = fields.Str()
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    approvedFor = fields.Str()
    firstName = fields.Str()
    lastName = fields.Str()
    mobile = fields.Str()
    country = fields.Str()
    dob = fields.Str()
    gpsTrack = fields.Str()
    verified = fields.Str()
    createdAt = fields.Str()
    activated = fields.Str()
    archived = fields.Nested(Archived())

    # @post_load
    # def make_user(self, data, **kwargs):
    #     id = data['_id'] if data['_id'] is not None else None
    #     return UserModel(data, id)

