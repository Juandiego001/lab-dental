from core.models import Warranty
from apiflask import Schema, fields
from marshmallow import post_load
from core.schemas.utils import BaseSchema


class WarrantyIn(BaseSchema):
    id = fields.Integer()
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    password = fields.String()
    status = fields.String(load_default='ACTIVE')


class WarrantyInCreate(WarrantyIn):
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    password = fields.String()

    @post_load
    def make_object(self, data, **kwargs):
        return Warranty(**data)


class WarrantyInUpdate(WarrantyIn):

    @post_load
    def make_object(self, data, **kwargs):
        return Warranty(**data)


class WarrantyOut(BaseSchema):
    id = fields.Integer()
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class WarrantiesOut(Schema):
    items = fields.List(fields.Nested(WarrantyOut))
