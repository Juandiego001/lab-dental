from core.models import Manual
from apiflask import Schema, fields
from marshmallow import post_load, pre_load
from core.schemas.utils import BaseSchema


class ManualIn(BaseSchema):
    id = fields.Integer()
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    password = fields.String()
    status = fields.String(load_default='ACTIVE')


class ManualInCreate(ManualIn):
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    password = fields.String()

    @post_load
    def make_object(self, data, **kwargs):
        return Manual(**data)


class ManualInUpdate(ManualIn):

    @post_load
    def make_object(self, data, **kwargs):
        return Manual(**data)


class ManualOut(BaseSchema):
    id = fields.Integer()
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class ManualsOut(Schema):
    items = fields.List(fields.Nested(ManualOut))
    total = fields.Integer()
