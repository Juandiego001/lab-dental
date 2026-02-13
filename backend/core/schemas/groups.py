from apiflask import Schema, fields
from marshmallow import ValidationError, post_load, pre_load, validate, validates_schema
from core.models import Group
from core.schemas.utils import BaseSchema

class GroupSearch(Schema):
    distributor_id = fields.Integer(
        required=False, allow_none=True, data_key='distributorId', load_default=None)
    name = fields.String(required=False, allow_none=True,
                         validate=validate.Length(max=50), load_default='')
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(data_key='perPage', load_default=15)

class GroupIn(BaseSchema):
    name = fields.String(required=True, allow_none=False,
                         validate=validate.Length(max=30))
    distributor_id = fields.Integer(required=False, allow_none=True, data_key='distributorId')
    users_ids = fields.List(fields.Integer, data_key='usersIds')
    status = fields.String(load_default='ACTIVE')

    @validates_schema
    def name_exists(self, data, **kwargs):
        '''
        Validate the name exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'name' in data:
            raise ValidationError({'message':  'Group name required'})

        if not data['name']:
            raise ValidationError({'message':  'Group name required'})


class GroupInCreate(GroupIn):
    @pre_load
    # Es posible que el grupo sea creado por un distribuidor, por lo tanto no se enviaría distributor_id sino que se tomaría del usuario
    def pop_null_distributor_id(self, data: dict, **kwargs):
        '''Remove null distributor_id'''

        if ('distributor_id' in data and not (data['distributor_id'])):
            data.pop('distributor_id')

        return data

    @post_load
    def make_object(self, data: dict, **kwargs):
        users_ids = data.pop('users_ids')
        return Group(**data), users_ids


class GroupInUpdate(GroupIn):
    id = fields.Integer()

    @pre_load
    # Es posible que el grupo sea creado por un distribuidor, por lo tanto no se enviaría distributor_id sino que se tomaría del usuario
    def pop_null_distributor_id(self, data: dict, **kwargs):
        '''Remove null distributor_id'''

        if ('distributor_id' in data and not (data['distributor_id'])):
            data.pop('distributor_id')

        return data

    @post_load
    def make_object(self, data: dict, **kwargs):
        users_ids = data.pop('users_ids')
        return Group(**data), users_ids


class GroupOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    distributor_id = fields.Integer(data_key='distributorId')
    distributor_name = fields.String(data_key='distributorName')
    users_ids = fields.List(fields.Integer, data_key='usersIds')
    status = fields.String()
    created_at = fields.DateTime(data_key='createdAt')
    updated_at = fields.DateTime(data_key='updatedAt')


class GroupsOut(Schema):
    items = fields.List(fields.Nested(GroupOut))
    total = fields.Integer()
