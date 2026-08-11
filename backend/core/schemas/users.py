
import re
from core.app import db
from apiflask import Schema
from core.models import User
from sqlalchemy import and_, or_
from bcrypt import hashpw, gensalt
from core.schemas.utils import BaseSchema, SortBy
from flask_jwt_extended import current_user
from apiflask.fields import Boolean, DateTime, File, Integer, List, Nested, String
from marshmallow import EXCLUDE, ValidationError, post_load, pre_load, validates_schema, validate
from flask_babel import gettext

class UsernameField(String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        
        if not re.match(r"^[a-zA-Z0-9._-]+$", value):
            raise ValidationError(gettext('invalidUsername'))
            
        return value
    
class EmailField(String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        
        if not re.match(r"^[a-zA-Z0-9@._-]+$", value):
            raise ValidationError(gettext('invalidEmail'))
            
        return value


class UserSearch(Schema):
    users_ids = List(Integer(), required=False, allow_none=True,
                     data_key='usersIds', load_default=None)
    distributor_id = Integer(
        required=False, allow_none=True, data_key='distributorId', load_default=None)
    is_main = Boolean(required=False, allow_none=True,
                      data_key='isMain', load_default=False)
    role = String(required=False, allow_none=True, load_default='')
    full_name = String(required=False, allow_none=True,
                       validate=validate.Length(max=50), data_key='fullName', load_default='')
    username = String(required=False, allow_none=True,
                      validate=validate.Length(max=20), load_default='')
    email = String(required=False, allow_none=True,
                   validate=validate.Length(max=150), load_default='')
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)

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
    email = EmailField()
    password = String()


class UserIn(BaseSchema):
    id = Integer()
    distributor_id = Integer(
        data_key='distributorId', required=False, allow_none=True)
    full_name = String(required=True, allow_none=False,
                       data_key='fullName', validate=validate.Length(max=50))
    username = UsernameField(required=True, allow_none=False,
                      validate=validate.Length(max=20))
    email = EmailField(required=True, allow_none=False,
                   validate=validate.Length(max=250))
    language = String(required=False,  validate=validate.Length(
        max=10), load_default='en')
    role = String(validate=validate.OneOf(choices=['ADMIN', 'DISTRIBUTOR']))
    password = String()
    status = String(load_default='ACTIVE')

    @validates_schema
    def full_name_exists(self, data, **kwargs):
        '''
        Validate the full name exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'full_name' in data:
            raise ValidationError({'message':  gettext('fullNameRequired')})

        if not data['full_name']:
            raise ValidationError({'message':  gettext('fullNameRequired')})

    @validates_schema
    def username_exists(self, data, **kwargs):
        '''
        Validate the username exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'username' in data:
            raise ValidationError({'message':  gettext('usernameRequired')})

        if not data['username']:
            raise ValidationError({'message':  gettext('usernameRequired')})

    @validates_schema
    def email_exists(self, data, **kwargs):
        '''
        Validate the email exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'email' in data:
            raise ValidationError({'message':  gettext('emailRequired')})

        if not data['email']:
            raise ValidationError({'message':  gettext('emailRequired')})

    @validates_schema
    def language_exists(self, data, **kwargs):
        '''
        Validate the language exists and if not set a value to en

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'language' in data:
            data['language'] = 'en'

        if not data['language']:
            data['language'] = 'en'

        return data


class UsersExistingIn(BaseSchema):
    search = String(required=False, allow_none=True, load_default='')
    users_ids = List(Integer(), required=False,
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
                {'message':  gettext('usernameEmailExist')})

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
                {'message':  gettext('usernameEmailExist')})

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
    id = Integer()
    distributor_id = Integer(data_key='distributorId')
    distributor_name = String(data_key='distributorName')
    full_name = String(data_key='fullName')
    username = String()
    email = String()
    language = String()
    role = String()
    status = String()
    created_at = DateTime(data_key='createdAt')
    updated_at = DateTime(data_key='updatedAt')


class UsersOut(Schema):
    items = List(Nested(UserOut))
    total = Integer()


class AbilitiesOut(Schema):
    action = String()
    subject = String()


class ProfileIn(Schema):
    class Meta:
        unknown = EXCLUDE

    full_name = String(required=True, data_key='fullName')
    username = String(required=True)
    email = String(required=True)
    language = String(required=True)


class ProfileOut(Schema):
    distributor_id = Integer()
    full_name = String(data_key='fullName')
    username = String()
    role = String()
    email = String()
    language = String()
    photo_path = String(data_key='photoPath')
    abilities = List(Nested(AbilitiesOut), dump_only=True)


class TokenIn(Schema):
    token = String()


class EmailIn(Schema):
    email = String()


class PasswordIn(Schema):
    current = String(required=True)
    new = String(required=True)

    @validates_schema
    def validation_1(self, data, **kwargs):
        '''Check if new password is valid'''

        new_pass = data['new']

        if not new_pass:
            return new_pass
        if not re.search(r'[A-Z]', new_pass):
            raise ValidationError({'message': gettext('mustHaveUppercase')})
        if not re.search(r'[a-z]', new_pass):
            raise ValidationError({'message': gettext('mustHaveLowerCase')})
        if not re.search(r'[^a-zA-Z0-9]', new_pass):
            raise ValidationError(
                {'message': gettext('mustHaveSpecialCharacter')})
        if not re.search(r"\d", new_pass):
            raise ValidationError({'message': gettext('mustHaveNumber')})
        if len(new_pass) < 10:
            raise ValidationError(
                {'message': gettext('mustHaveMinimum10Characters')})
        if len(new_pass) > 24:
            raise ValidationError(
                {'message': gettext('mustHaveMaximum24Characters')})
        return data

    @validates_schema
    def validation_2(self, data, **kwargs):
        '''Check if current password is valid'''

        if not current_user.check_password(data['current']):
            raise ValidationError(
                {'message':  gettext('invalidCurrentPassword')})

    @post_load
    def make_object(self, data, **kwargs):
        '''Make User object with new password'''

        new_password = data['new'].encode('utf-8')
        new_password = hashpw(new_password, gensalt()).decode('utf-8')
        return User(id=current_user.id, password=new_password)


class TokenPasswordIn(Schema):
    token = String()
    password = String()

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


class PhotoIn(Schema):
    photo = File(required=True)