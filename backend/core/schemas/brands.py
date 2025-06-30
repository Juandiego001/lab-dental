from core.models import Brand
from apiflask import Schema, fields
from marshmallow import post_load
from core.schemas.utils import BaseSchema


class BrandIn(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    slug = fields.String()
    status = fields.String(load_default='ACTIVE')


class BrandInCreate(BrandIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Brand(**data)


class BrandInUpdate(BrandIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Brand(**data)


class BrandOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    slug = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class BrandsOut(Schema):
    items = fields.List(fields.Nested(BrandOut))
    total = fields.Integer()
