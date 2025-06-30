from core.models import Address, Site
from apiflask import Schema, fields
from marshmallow import post_load, validates_schema
from core.schemas.utils import BaseSchema
from werkzeug.exceptions import HTTPException


class SiteIn(BaseSchema):
    distributor_id = fields.Integer(
        data_key='distributorId', required=False, allow_none=True)
    client_id = fields.Integer(
        data_key='clientId', required=False, allow_none=True)
    city_id = fields.Integer(data_key='cityId')
    description = fields.String()
    name = fields.String()
    status = fields.String(load_default='ACTIVE')


class SiteInCreate(SiteIn):
    @validates_schema
    def distributor_id_or_client_id(self, data: dict, **kwargs):
        '''There must be either a distributor id or a client id'''

        if ('distributor_id' in data and not data['distributor_id']) and ('client_id' in data and not data['client_id']):
            raise HTTPException('Distributor ID or Client ID required')

        if 'distributor_id' in data and not data['distributor_id']:
            data.pop('distributor_id')

        if 'client_id' in data and not data['client_id']:
            data.pop('client_id')

    @post_load
    def make_object(self, data: dict, **kwargs):
        city_id = data.pop('city_id')
        description = data.pop('description')
        return Address(city_id=city_id, description=description), Site(**data)


class SiteInUpdate(SiteIn):
    id = fields.Integer()
    address_id = fields.Integer(data_key='addressId')

    @validates_schema
    def distributor_id_or_client_id(self, data: dict, **kwargs):
        '''There must be either a distributor id or a client id'''

        if ('distributor_id' in data and not data['distributor_id']) and ('client_id' in data and not data['client_id']):
            raise HTTPException('Distributor ID or Client ID required')

        if 'distributor_id' in data and not data['distributor_id']:
            data.pop('distributor_id')

        if 'client_id' in data and not data['client_id']:
            data.pop('client_id')

    @post_load
    def make_object(self, data: dict, **kwargs):
        address_id = data.pop('address_id')
        city_id = data.pop('city_id')
        description = data.pop('description')
        return Address(id=address_id, city_id=city_id, description=description), Site(**data)


class SiteOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    address_id = fields.Integer(data_key='addressId')
    description = fields.String()
    status = fields.String()
    country_id = fields.Integer(data_key='countryId')
    country_name = fields.String(data_key='countryName')
    state_id = fields.Integer(data_key='stateId')
    state_name = fields.String(data_key='stateName')
    city_id = fields.Integer(data_key='cityId')
    city_name = fields.String(data_key='cityName')
    distributor_client = fields.String(data_key='distributorClient')
    created_at = fields.DateTime(data_key='createdAt')
    updated_at = fields.DateTime(data_key='updatedAt')


class SitesOut(Schema):
    items = fields.List(fields.Nested(SiteOut))
    total = fields.Integer()
