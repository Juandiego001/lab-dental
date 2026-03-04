from core.models import Category
from apiflask import Schema, fields
from marshmallow import ValidationError, post_load, validates_schema, validate
from core.schemas.utils import BaseSchema
from flask_babel import gettext


class CategorySearch(Schema):
    category_id = fields.Integer(required=False, allow_none=True, data_key='categoryId', load_default=None)
    name = fields.String(required=False, allow_none=True,
                         validate=validate.Length(max=50), load_default='')
    slug = fields.String(required=False, allow_none=True,
                          validate=validate.Length(max=50), load_default='')
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(data_key='perPage', load_default=15)


class CategoryIn(BaseSchema):
    id = fields.Integer()
    name = fields.String(required=True, allow_none=False, validate=validate.Length(max=50))
    slug = fields.String(required=True, allow_none=False, validate=validate.Length(max=50))
    status = fields.String(load_default='ACTIVE')

    @validates_schema
    def name_exists(self, data, **kwargs):
        '''
        Validate the name exists and have a value
        
        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'name' in data :
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

        if not 'slug' in data :
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
    id = fields.Integer()
    name = fields.String()
    slug = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class CategoriesOut(Schema):
    items = fields.List(fields.Nested(CategoryOut))
    total = fields.Integer()
