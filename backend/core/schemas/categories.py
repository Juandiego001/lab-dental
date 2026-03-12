from core.models import Category
from apiflask import Schema
from apiflask.fields import Integer, String, Nested, List, DateTime
from marshmallow import ValidationError, post_load, validates_schema, validate
from core.schemas.utils import BaseSchema, SortBy
from flask_babel import gettext


class CategorySearch(Schema):
    category_id = Integer(required=False, allow_none=True,
                          data_key='categoryId', load_default=None)
    name = String(required=False, allow_none=True,
                  validate=validate.Length(max=50), load_default='')
    slug = String(required=False, allow_none=True,
                  validate=validate.Length(max=50), load_default='')
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)


class CategoryIn(BaseSchema):
    id = Integer()
    name = String(required=True, allow_none=False,
                  validate=validate.Length(max=50))
    slug = String(required=True, allow_none=False,
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
            raise ValidationError({'message':  gettext('nameRequired')})

        if not data['name']:
            raise ValidationError({'message':  gettext('nameRequired')})

    @validates_schema
    def slug_exists(self, data, **kwargs):
        '''
        Validate the slug exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'slug' in data:
            raise ValidationError({'message':  gettext('slugRequired')})

        if not data['slug']:
            raise ValidationError({'message':  gettext('slugRequired')})


class CategoryInCreate(CategoryIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Category(**data)


class CategoryInUpdate(CategoryIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Category(**data)


class CategoryOut(BaseSchema):
    id = Integer()
    name = String()
    slug = String()
    status = String()
    created_at = DateTime()
    updated_at = DateTime()


class CategoriesOut(Schema):
    items = List(Nested(CategoryOut))
    total = Integer()
