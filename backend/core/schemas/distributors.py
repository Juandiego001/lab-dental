from core.models import Distributor
from apiflask import Schema, fields
from marshmallow import post_load, validates_schema
from core.schemas.utils import BaseSchema


class DistributorIn(BaseSchema):
    id = fields.Integer()
    name = fields.String(allow_none=False, validate=lambda v: v != '')
    status = fields.String(load_default='ACTIVE')


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
