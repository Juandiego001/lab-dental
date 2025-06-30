from apiflask import Schema, fields
from marshmallow import post_load, pre_load
from core.models import Group
from core.schemas.utils import BaseSchema


class GroupIn(BaseSchema):
    name = fields.String()
    distributor_id = fields.Integer(data_key='distributorId')
    users_ids = fields.List(fields.Integer, data_key='usersIds')
    status = fields.String(load_default='ACTIVE')


class GroupInCreate(GroupIn):
    @pre_load
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
    pass


class GroupOut(BaseSchema):
    id = fields.Integer()
    distributor_name = fields.String(required=False, data_key='distributorName')
    name = fields.String()
    users_ids = fields.List(fields.Integer, data_key='usersIds')
    status = fields.String()
    created_at = fields.DateTime(data_key='createdAt')
    updated_at = fields.DateTime(data_key='updatedAt')


class GroupsOut(Schema):
    items = fields.List(fields.Nested(GroupOut))
    total = fields.Integer()
