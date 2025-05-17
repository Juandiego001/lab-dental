from core.models import Client
from apiflask import Schema, fields
from marshmallow import post_load
from core.schemas.utils import BaseSchema


class ClientIn(BaseSchema):
    id = fields.Integer()
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    password = fields.String()
    status = fields.String(load_default='ACTIVE')


class ClientInCreate(ClientIn):
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    password = fields.String()

    @post_load
    def make_object(self, data, **kwargs):
        return Client(**data)


class ClientInUpdate(ClientIn):

    @post_load
    def make_object(self, data, **kwargs):
        return Client(**data)


class ClientOut(BaseSchema):
    id = fields.Integer()
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class ClientsOut(Schema):
    items = fields.List(fields.Nested(ClientOut))
