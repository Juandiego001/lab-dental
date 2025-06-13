from core.models import Address, Site
from apiflask import Schema, fields
from marshmallow import post_load, validates
from core.schemas.utils import BaseSchema
from werkzeug.exceptions import HTTPException


class SiteIn(BaseSchema):
    id = fields.Integer()
    distributor_id = fields.Integer(data_key='distributorId', required=False)
    client_id = fields.Integer(data_key='clientId', required=False)
    city_id = fields.Integer(data_key='cityId')
    description = fields.String()
    name = fields.String()
    status = fields.String(load_default='ACTIVE')


class SiteInCreate(SiteIn):
    # @validaes
    # def validate_distributor_or_client(self, data, **kwargs):
    #     print(data)
    #     if not data['distributor_id'] and not data['client_id']:
    #         raise HTTPException('Not valid distributor_id or client_id')

    @post_load
    def make_object(self, data: dict, **kwargs):
        city_id = data.pop('city_id')
        description = data.pop('description')
        return Address(city_id=city_id, description=description), Site(**data)


class SiteInUpdate(SiteIn):

    @post_load
    def make_object(self, data, **kwargs):
        return Site(**data)


class SiteOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    status = fields.String()
    distributor_client = fields.String(data_key='distributorClient')
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class SitesOut(Schema):
    items = fields.List(fields.Nested(SiteOut))
    total = fields.Integer()
