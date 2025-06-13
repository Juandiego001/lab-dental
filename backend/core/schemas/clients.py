from core.models import Client
from apiflask import Schema, fields
from marshmallow import post_load
from core.schemas.utils import BaseSchema


class DistributorClient(Schema):
    id = fields.Integer()
    name = fields.String(required=False)


class ClientIn(BaseSchema):
    id = fields.Integer()
    distributor = fields.Nested(DistributorClient)
    name = fields.String()
    phone = fields.String()
    status = fields.String(load_default='ACTIVE')


class ClientInCreate(ClientIn):
    @post_load
    def make_object(self, data, **kwargs):
        data['distributor_id'] = data.pop('distributor')['id']
        return Client(**data)


class ClientInUpdate(ClientIn):
    @post_load
    def make_object(self, data, **kwargs):
        data['distributor_id'] = data.pop('distributor')['id']
        return Client(**data)


class ClientOut(BaseSchema):
    id = fields.Integer()
    distributor = fields.Nested(DistributorClient)
    name = fields.String()
    phone = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class ClientsOut(Schema):
    items = fields.List(fields.Nested(ClientOut))
    total = fields.Integer()
