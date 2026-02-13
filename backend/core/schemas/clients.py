from core.models import Client
from apiflask import Schema, fields
from marshmallow import post_load, pre_load, validates_schema, ValidationError, validate
from core.schemas.utils import BaseSchema


class ClientSearch(Schema):
    distributor_id = fields.Integer(
        required=False, allow_none=True, data_key='distributorId', load_default=None)
    client_id = fields.Integer(
        required=False, allow_none=True, data_key='clientId', load_default=None)
    name = fields.String(required=False, allow_none=True,
                         validate=validate.Length(max=50), load_default='')
    phone = fields.String(required=False, allow_none=True,
                          validate=validate.Length(max=20), load_default='')
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(data_key='perPage', load_default=15)


class ClientIn(BaseSchema):
    id = fields.Integer()
    distributor_id = fields.Integer(
        required=False, allow_none=True, data_key='distributorId')
    name = fields.String(required=True, allow_none=False,
                         validate=validate.Length(max=50))
    phone = fields.String(required=True, allow_none=False,
                          validate=validate.Length(max=20))
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
            raise ValidationError({'message':  "Client's name required"})

        if not data['name']:
            raise ValidationError({'message':  "Client's name required"})

    @validates_schema
    def phone_exists(self, data, **kwargs):
        '''
        Validate the phone exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'phone' in data:
            raise ValidationError({'message':  "Client's phone required"})

        if not data['phone']:
            raise ValidationError({'message':  "Client's phone required"})


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
    id = fields.Integer()
    distributor_id = fields.Integer(data_key='distributorId')
    distributor_name = fields.String(data_key='distributorName')
    name = fields.String()
    phone = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class ClientsOut(Schema):
    items = fields.List(fields.Nested(ClientOut))
    total = fields.Integer()
