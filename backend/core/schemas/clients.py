from core.models import Client
from apiflask import Schema, fields
from apiflask.fields import DateTime, Integer, String, List, Nested
from marshmallow import post_load, pre_load, validates_schema, ValidationError, validate
from core.schemas.utils import BaseSchema, SortBy
from flask_babel import gettext


class ClientSearch(Schema):
    distributor_id = Integer(
        required=False, allow_none=True, data_key='distributorId', load_default=None)
    client_id = Integer(
        required=False, allow_none=True, data_key='clientId', load_default=None)
    name = String(required=False, allow_none=True,
                  validate=validate.Length(max=50), load_default='')
    phone = String(required=False, allow_none=True,
                   validate=validate.Length(max=20), load_default='')
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)


class ClientIn(BaseSchema):
    id = Integer()
    distributor_id = Integer(
        required=False, allow_none=True, data_key='distributorId')
    name = String(required=True, allow_none=False,
                  validate=validate.Length(max=50))
    phone = String(required=True, allow_none=False,
                   validate=validate.Length(max=20))
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
            raise ValidationError({'message':  gettext('clientNameRequired')})

        if not data['name']:
            raise ValidationError({'message':  gettext('clientNameRequired')})

    @validates_schema
    def phone_exists(self, data, **kwargs):
        '''
        Validate the phone exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'phone' in data:
            raise ValidationError({'message':  gettext('clientPhoneRequired')})

        if not data['phone']:
            raise ValidationError({'message':  gettext('clientPhoneRequired')})


class ClientInCreate(ClientIn):
    @pre_load
    def verify_distributor_id_none(self, data: dict, **kwargs):
        '''Pop distributor_id if is none'''

        if 'distributor_id' in data and not (data['distributor_id']):
            data.pop('distributor_id')

        return data

    @post_load
    def make_object(self, data, **kwargs):
        return Client(**data)


class ClientInUpdate(ClientIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Client(**data)


class ClientOut(BaseSchema):
    id = Integer()
    distributor_id = Integer(data_key='distributorId')
    distributor_name = String(data_key='distributorName')
    name = String()
    phone = String()
    status = String()
    created_at = DateTime()
    updated_at = DateTime()


class ClientsOut(Schema):
    items = List(Nested(ClientOut))
    total = Integer()
