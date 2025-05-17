from bcrypt import hashpw, gensalt
from core.models import User
from apiflask import Schema, fields
from marshmallow import post_load, pre_load
from core.schemas.utils import BaseSchema


class UserInLogIn(BaseSchema):
    email = fields.String()
    password = fields.String()


class UserIn(BaseSchema):
    id = fields.Integer()
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    password = fields.String()
    status = fields.String(load_default='ACTIVE')


class UserInCreate(UserIn):
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    password = fields.String()

    @pre_load
    def config(self, data, **kwargs):
        new_password = data['password'].encode('utf-8')
        new_password = hashpw(new_password, gensalt()).decode('utf-8')
        data['password'] = new_password
        data['status'] = 'ACTIVE'
        return data

    @post_load
    def make_object(self, data, **kwargs):
        return User(**data)


class UserInUpdate(UserIn):

    @post_load
    def make_object(self, data, **kwargs):
        return User(**data)


class UserOut(BaseSchema):
    id = fields.Integer()
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class UsersOut(Schema):
    items = fields.List(fields.Nested(UserOut))


class AbilitiesOut(Schema):
    action = fields.String()
    subject = fields.String()


class ProfileIn(Schema):
    full_name = fields.String()

    @post_load
    def make_object(self, data, **kwargs):
        return User(**data)


class ProfileOut(Schema):
    full_name = fields.String()
    email = fields.String()
    abilities = fields.List(fields.Nested(AbilitiesOut), dump_only=True)
