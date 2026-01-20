from bcrypt import hashpw, gensalt
from core.models import List_
from apiflask import Schema, fields
from marshmallow import post_load, pre_load
from core.schemas.utils import BaseSchema


class ListIn(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    distributors_ids = fields.List(fields.Integer, data_key='distributorsIds')
    users_ids = fields.List(fields.Integer, data_key='usersIds', required=False, allow_none=True)
    status = fields.String(load_default='ACTIVE')


class ListOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    is_main = fields.Boolean(data_key='isMain')
    distributors_ids = fields.List(fields.Integer, data_key='distributorsIds')
    users_ids = fields.List(fields.Integer, data_key='usersIds')
    slug = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class ListsOut(Schema):
    items = fields.List(fields.Nested(ListOut))
    total = fields.Integer()
