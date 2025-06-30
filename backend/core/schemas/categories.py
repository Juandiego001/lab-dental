from core.models import Category
from apiflask import Schema, fields
from marshmallow import post_load
from core.schemas.utils import BaseSchema


class CategoryIn(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    slug = fields.String()
    status = fields.String(load_default='ACTIVE')


class CategoryInCreate(CategoryIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Category(**data)


class CategoryInUpdate(CategoryIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Category(**data)


class CategoryOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    slug = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class CategoriesOut(Schema):
    items = fields.List(fields.Nested(CategoryOut))
    total = fields.Integer()
