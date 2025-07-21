from bcrypt import hashpw, gensalt
from sqlalchemy import or_
from core.app import db
from core.models import User
from apiflask import Schema, abort, fields
from marshmallow import post_load, pre_load, validates_schema
from core.schemas.utils import BaseSchema
from werkzeug.exceptions import HTTPException


class UserInLogIn(BaseSchema):
    email = fields.String()
    password = fields.String()


class UserIn(BaseSchema):
    id = fields.Integer()
    distributor_id = fields.Integer(
        data_key='distributorId', required=False, allow_none=True)
    full_name = fields.String(data_key='fullName')
    username = fields.String()
    email = fields.String()
    role = fields.String()
    password = fields.String()
    status = fields.String(load_default='ACTIVE')


class UserInCreate(UserIn):
    @pre_load
    def check_email_or_username_exists(self, data, **kwargs):
        '''Check if there is already a user with the username or the email given'''

        user = db.session.query(User)\
            .filter(or_(User.email == data['email'], User.username == data['username']))\
            .first()

        if user:
            abort(400, 'Username or email already exists')

        return data

    @pre_load
    def set_password(self, data: dict, **kwargs):
        '''Set the password'''

        new_password = data['password'].encode('utf-8')
        new_password = hashpw(new_password, gensalt()).decode('utf-8')
        data['password'] = new_password
        data['status'] = 'ACTIVE'
        return data

    @pre_load
    def if_role_not_exists(self, data, **kwargs):
        '''If role not exists set DISTRIBUTOR role'''

        if not 'role' in data or not data['role']:
            data['role'] = 'DISTRIBUTOR'
        return data

    @post_load
    def make_object(self, data: dict, **kwargs):
        distributor_id = data.pop('distributor_id')
        return User(**data), distributor_id


class UserInUpdate(UserIn):
    @pre_load
    def check_email_or_username_exists(self, data, **kwargs):
        '''Check if there is already a user with the username or the email given'''

        current_user: User = db.session.query(
            User).filter(User.id == data['id']).first()

        user_exists = None
        if current_user.email != data['email'] and current_user.email != data['username']:
            user_exists = db.session.query(User)\
                .filter(or_(User.email == data['email'], User.username == data['username']))\
                .first()
        elif current_user.email != data['email']:
            user_exists = db.session.query(User)\
                .filter(User.email == data['email'])\
                .first()
        elif current_user.username != data['username']:
            user_exists = db.session.query(User)\
                .filter(User.username == data['username'])\
                .first()

        if user_exists:
            abort(400, 'Username or email already exists')

        return data

    @pre_load
    def set_password(self, data: dict, **kwargs):

        if 'password' in data and data['password']:
            new_password = data['password'].encode('utf-8')
            new_password = hashpw(new_password, gensalt()).decode('utf-8')
            data['password'] = new_password

        return data

    @post_load
    def make_object(self, data: dict, **kwargs):
        distributor_id = data.pop('distributor_id')
        return User(**data), distributor_id


class UserOut(BaseSchema):
    id = fields.Integer()
    distributor_id = fields.Integer(data_key='distributorId')
    distributor_name = fields.String(data_key='distributorName')
    full_name = fields.String(data_key='fullName')
    username = fields.String()
    email = fields.String()
    role = fields.String()
    status = fields.String()
    created_at = fields.DateTime(data_key='createdAt')
    updated_at = fields.DateTime(data_key='updatedAt')


class UsersOut(Schema):
    items = fields.List(fields.Nested(UserOut))
    total = fields.Integer()


class AbilitiesOut(Schema):
    action = fields.String()
    subject = fields.String()


class ProfileIn(Schema):
    full_name = fields.String()

    @post_load
    def make_object(self, data, **kwargs):
        return User(**data)


class ProfileOut(Schema):
    distributor_id = fields.Integer()
    full_name = fields.String()
    role = fields.String()
    email = fields.String()
    abilities = fields.List(fields.Nested(AbilitiesOut), dump_only=True)
