from apiflask import Schema
from apiflask.fields import Integer, String, Nested, List, DateTime, Function
from core.models import Address, Site
from core.schemas.utils import BaseSchema, SortBy
from marshmallow import ValidationError, post_load, validates_schema, validate
from flask_babel import gettext


class SiteSearch(Schema):
    site_id = Integer(
        required=False, allow_none=True, data_key='siteId', load_default=None)
    distributor_id = Integer(
        required=False, allow_none=True, data_key='distributorId', load_default=None)
    client_id = Integer(
        required=False, allow_none=True, data_key='clientId', load_default=None)
    name = String(required=False, allow_none=True,
                  validate=validate.Length(max=50), load_default='')
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)


class SiteIn(BaseSchema):
    distributor_id = Integer(
        data_key='distributorId', required=False, allow_none=True)
    client_id = Integer(
        data_key='clientId', required=False, allow_none=True)
    country_id = Integer(data_key='countryId')
    state_id = Integer(
        required=False, allow_none=True, data_key='stateId')
    city_id = Integer(
        required=False, allow_none=True, data_key='cityId')
    description = String(
        required=True, allow_none=False, validate=validate.Length(max=255))
    name = String(required=True, allow_none=False,
                  validate=validate.Length(max=50))
    status = String(load_default='ACTIVE')

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
    id = Integer()
    address_id = Integer(data_key='addressId')

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
    id = Integer()
    name = String()
    distributor_id = Integer(data_key='distributorId')
    client_id = Integer(data_key='clientId')
    address_id = Integer(data_key='addressId')
    description = String()
    status = String()
    country_id = Integer(data_key='countryId')
    country_name = String(data_key='countryName')
    state_id = Integer(required=False, data_key='stateId')
    state_name = String(required=False, data_key='stateName')
    city_id = Integer(required=False, data_key='cityId')
    city_name = String(required=False, data_key='cityName')
    client_name = String(data_key='clientName')
    distributor_name = String(data_key='distributorName')
    created_at = DateTime(data_key='createdAt')
    updated_at = DateTime(data_key='updatedAt')
    company_type = Function(
        lambda data: 'distributors' if data.distributor_id else 'clients', data_key='companyType')
    distributor_client = String(data_key='distributorClient')


class SitesOut(BaseSchema):
    items = List(Nested(SiteOut))
    total = Integer()


class SiteInstallationOut(BaseSchema):
    id = Integer()
    name = String()


class SitesInstallationsOut(BaseSchema):
    items = List(Nested(SiteInstallationOut))
