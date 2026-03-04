from core.models import Distributor
from apiflask import Schema, fields
from marshmallow import post_load, validates_schema, ValidationError, validate
from core.schemas.utils import BaseSchema
from flask_babel import gettext


class DistributorSearch(Schema):
    distributors_ids = fields.List(fields.Integer(required=False, allow_none=True, load_default=None),
                                   required=False, allow_none=True, data_key='distributorsIds', load_default=None)
    name = fields.String(required=False, allow_none=True,
                         validate=validate.Length(max=50), load_default='')
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(data_key='perPage', load_default=15)

    @validates_schema
    def validate_distributors_ids(self, data: dict, **kwargs):
        '''
        Docstring for validate_distributors_ids
        
        :param self: Description
        :param data: Description
        :type data: dict
        :param kwargs: Description
        '''

        if not 'distributors_ids' in data:
            return data
        
        if not data['distributors_ids']:
            return data
            
        for i in data['distributors_ids']:
            if i != None:
                return data
        
        data['distributors_ids'] = None
        return data


class DistributorIn(BaseSchema):
    id = fields.Integer()
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
            raise ValidationError({'message':  gettext('distributorNameRequired')})

        if not data['name']:
            raise ValidationError({'message':  gettext('distributorNameRequired')})


class DistributorInCreate(DistributorIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Distributor(**data)


class DistributorInUpdate(DistributorIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Distributor(**data)


class DistributorOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    status = fields.String()
    created_at = fields.DateTime(data_key='createdAt')
    updated_at = fields.DateTime(data_key='updatedAt')


class DistributorsOut(Schema):
    items = fields.List(fields.Nested(DistributorOut))
    total = fields.Integer()


class DistributorsExistingIn(BaseSchema):
    search = fields.String(required=False)
    distributors_ids = fields.List(fields.Integer(
    ), required=False, allow_none=True, load_default=[], data_key='distributorsIds')

    @validates_schema
    def validate_distributors_ids(self, data, **kwargs):
        if 'distributors_ids' in data and not data['distributors_ids']:
            data['distributors_ids'] = []

        return data
