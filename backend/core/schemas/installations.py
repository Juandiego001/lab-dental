from bcrypt import hashpw, gensalt
from core.models import Installation
from apiflask import Schema, fields
from marshmallow import post_load, pre_load
from core.schemas.utils import BaseSchema


class InstallationIn(BaseSchema):
    id = fields.Integer()
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    password = fields.String()
    status = fields.String(load_default='ACTIVE')


class InstallationInCreate(InstallationIn):
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    password = fields.String()

    @post_load
    def make_object(self, data, **kwargs):
        return Installation(**data)


class InstallationInUpdate(InstallationIn):

    @post_load
    def make_object(self, data, **kwargs):
        return Installation(**data)


class InstallationOut(BaseSchema):
    id = fields.Integer()
    full_name = fields.String(data_key='fullName')
    email = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class InstallationsOut(Schema):
    items = fields.List(fields.Nested(InstallationOut))
    total = fields.Integer()
