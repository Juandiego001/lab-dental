from apiflask import Schema, fields
from core.models import Address, Site
from core.schemas.utils import BaseSchema
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError, post_load, validates_schema, validate
from flask_babel import gettext


class SiteSearch(Schema):
    site_id = fields.Integer(
        required=False, allow_none=True, data_key='siteId', load_default=None)
    distributor_id = fields.Integer(
        required=False, allow_none=True, data_key='distributorId', load_default=None)
    client_id = fields.Integer(
        required=False, allow_none=True, data_key='clientId', load_default=None)
    name = fields.String(required=False, allow_none=True,
                         validate=validate.Length(max=50), load_default='')
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(data_key='perPage', load_default=15)


class SiteIn(BaseSchema):
    distributor_id = fields.Integer(
        data_key='distributorId', required=False, allow_none=True)
    client_id = fields.Integer(
        data_key='clientId', required=False, allow_none=True)
    country_id = fields.Integer(data_key='countryId')
    state_id = fields.Integer(
        required=False, allow_none=True, data_key='stateId')
    city_id = fields.Integer(
        required=False, allow_none=True, data_key='cityId')
    description = fields.String(
        required=True, allow_none=False, validate=validate.Length(max=255))
    name = fields.String(required=True, allow_none=False,
                         validate=validate.Length(max=50))
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
            raise ValidationError({'message':  gettext('siteNameRequired')})

        if not data['name']:
            raise ValidationError({'message':  gettext('siteNameRequired')})

    @validates_schema
    def description_exists(self, data, **kwargs):
        '''
        Validate the description exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'description' in data:
            raise ValidationError({'message':  gettext('siteAddressRequired')})

        if not data['description']:
            raise ValidationError({'message':  gettext('siteAddressRequired')})


class SiteInCreate(SiteIn):
    @validates_schema
    def distributor_id_or_client_id(self, data: dict, **kwargs):
        '''There must be either a distributor id or a client id'''

        if 'distributor_id' in data and not data['distributor_id']:
            data.pop('distributor_id')

        if 'client_id' in data and not data['client_id']:
            data.pop('client_id')

        if 'distributor_id' in data:
            return data

        if 'client_id' in data:
            return data

    @post_load
    def make_object(self, data: dict, **kwargs):
        country_id = data.pop('country_id')
        state_id = data.pop('state_id')
        city_id = data.pop('city_id') if 'city_id' in data else None
        description = data.pop('description')
        return Address(country_id=country_id, state_id=state_id, city_id=city_id, description=description), Site(**data)


class SiteInUpdate(SiteIn):
    id = fields.Integer()
    address_id = fields.Integer(data_key='addressId')

    @validates_schema
    def distributor_id_or_client_id(self, data: dict, **kwargs):
        '''There must be either a distributor id or a client id'''

        if 'distributor_id' in data and not data['distributor_id']:
            data.pop('distributor_id')

        if 'client_id' in data and not data['client_id']:
            data.pop('client_id')

        if 'distributor_id' in data:
            return data

        if 'client_id' in data:
            return data

        raise ValidationError(
            {'message':  gettext('clientIddistributorIdRequired')})

    @post_load
    def make_object(self, data: dict, **kwargs):
        address_id = data.pop('address_id')
        country_id = data.pop('country_id')
        state_id = data.pop('state_id')
        city_id = data.pop('city_id')
        description = data.pop('description')
        return Address(id=address_id, country_id=country_id, state_id=state_id, city_id=city_id, description=description), Site(**data)


class SiteOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    distributor_id = fields.Integer(data_key='distributorId')
    client_id = fields.Integer(data_key='clientId')
    address_id = fields.Integer(data_key='addressId')
    description = fields.String()
    status = fields.String()
    country_id = fields.Integer(data_key='countryId')
    country_name = fields.String(data_key='countryName')
    state_id = fields.Integer(required=False, data_key='stateId')
    state_name = fields.String(required=False, data_key='stateName')
    city_id = fields.Integer(required=False, data_key='cityId')
    city_name = fields.String(required=False, data_key='cityName')
    client_name = fields.String(data_key='clientName')
    distributor_name = fields.String(data_key='distributorName')
    created_at = fields.DateTime(data_key='createdAt')
    updated_at = fields.DateTime(data_key='updatedAt')
    company_type = fields.Function(
        lambda data: 'distributors' if data.distributor_id else 'clients', data_key='companyType')
    distributor_client = fields.Function(
        lambda data: data._mapping['distributor_name'] if data._mapping['distributor_name'] else data._mapping['client_name'], data_key='distributorClient')


class SitesOut(BaseSchema):
    items = fields.List(fields.Nested(SiteOut))
    total = fields.Integer()


class SiteInstallationOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()


class SitesInstallationsOut(BaseSchema):
    items = fields.List(fields.Nested(SiteInstallationOut))
