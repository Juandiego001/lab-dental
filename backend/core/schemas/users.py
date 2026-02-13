from bcrypt import hashpw, gensalt
from sqlalchemy import and_, or_
from core.app import db
from core.models import User
from apiflask import Schema, fields
from marshmallow import ValidationError, post_load, pre_load, validates_schema, validate
from core.schemas.utils import BaseSchema
from werkzeug.exceptions import HTTPException



class UserSearch(Schema):
    users_ids = fields.List(fields.Integer(), required=False, allow_none=True, data_key='usersIds', load_default=None)
    distributor_id = fields.Integer(
        required=False, allow_none=True, data_key='distributorId', load_default=None)
    is_main = fields.Boolean(required=False, allow_none=True, data_key='isMain', load_default=False)
    role = fields.String(required=False, allow_none=True, load_default='')
    full_name = fields.String(required=False, allow_none=True,
                         validate=validate.Length(max=50), data_key='fullName', load_default='')
    username = fields.String(required=False, allow_none=True,
                          validate=validate.Length(max=20), load_default='')
    email = fields.String(required=False, allow_none=True, validate=validate.Length(max=250), load_default='')
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(data_key='perPage', load_default=15)

    @validates_schema
    def validate_users_ids(self, data: dict, **kwargs):
        '''
        Docstring for validate_users_ids
        
        :param self: Description
        :param data: Description
        :type data: dict
        :param kwargs: Description
        '''

        if not 'users_ids' in data:
            return data
        
        if not data['users_ids']:
            return data
            
        for i in data['users_ids']:
            if i != None:
                return data
        
        data['users_ids'] = None
        return data


class UserInLogIn(BaseSchema):
    email = fields.String()
    password = fields.String()


class UserIn(BaseSchema):
    id = fields.Integer()
    distributor_id = fields.Integer(
        data_key='distributorId', required=False, allow_none=True)
    full_name = fields.String(required=True, allow_none=False, data_key='fullName', validate=validate.Length(max=50))
    username = fields.String(required=True, allow_none=False, validate=validate.Length(max=20))
    email = fields.String(required=True, allow_none=False, validate=validate.Length(max=250))
    role = fields.String()
    password = fields.String()
    status = fields.String(load_default='ACTIVE')

    @validates_schema
    def full_name_exists(self, data, **kwargs):
        '''
        Validate the full name exists and have a value
        
        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'full_name' in data :
            raise ValidationError({'message':  'Full name required'})
        
        if not data['full_name']:
            raise ValidationError({'message':  'Full name required'})


    @validates_schema
    def username_exists(self, data, **kwargs):
        '''
        Validate the username exists and have a value
        
        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'username' in data :
            raise ValidationError({'message':  'Username required'})
        
        if not data['username']:
            raise ValidationError({'message':  'Username required'})


    @validates_schema
    def email_exists(self, data, **kwargs):
        '''
        Validate the email exists and have a value
        
        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'email' in data :
            raise ValidationError({'message':  'Email required'})
        
        if not data['email']:
            raise ValidationError({'message':  'Email required'})


class UsersExistingIn(BaseSchema):
    search = fields.String(required=False, allow_none=True, load_default='')
    users_ids = fields.List(fields.Integer(), required=False,
                            allow_none=True, load_default=[], data_key='usersIds')

    @validates_schema
    def validate_users_ids(self, data, **kwargs):
        if 'users_ids' in data and not data['users_ids']:
            data['users_ids'] = []

        return data


class UserInCreate(UserIn):
    @pre_load
    def check_email_or_username_exists(self, data, **kwargs):
        '''Check if there is already a user with the username or the email given'''

        user = db.session.query(User)\
            .filter(and_(or_(User.email == data['email'], User.username == data['username']), User.status == 'ACTIVE'))\
            .first()

        if user:
            raise ValidationError(
                {'message':  'Username or email already exists'})

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
                .filter(and_(or_(User.email == data['email'], User.username == data['username']), User.status == 'ACTIVE'))\
                .first()
        elif current_user.email != data['email']:
            user_exists = db.session.query(User)\
                .filter(and_(User.email == data['email'], User.status == 'ACTIVE'))\
                .first()
        elif current_user.username != data['username']:
            user_exists = db.session.query(User)\
                .filter(and_(User.username == data['username'], User.status == 'ACTIVE'))\
                .first()

        if user_exists:
            raise ValidationError(
                {'message':  'Username or email already exists'})

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


class TokenIn(Schema):
    token = fields.String()

class EmailIn(Schema):
    email = fields.String()

class PasswordIn(Schema):
    token = fields.String()
    password = fields.String()

    @pre_load
    def convert_password(self, data, **kwargs):
        '''
        Docstring for convert_password
        
        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        new_password = data['password'].encode('utf-8')
        new_password = hashpw(new_password, gensalt()).decode('utf-8')
        data['password'] = new_password
        return data