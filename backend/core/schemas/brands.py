from core.models import Brand
from apiflask import Schema
from apiflask.fields import DateTime, Integer, List, Nested, String
from marshmallow import ValidationError, post_load, validate, validates_schema
from core.schemas.utils import BaseSchema, SortBy
from flask_babel import gettext


class BrandSearch(Schema):
    brands_ids = List(Integer(required=False, allow_none=True, load_default=None),
                            required=False, allow_none=True, data_key='brandsIds', load_default=None)
    name = String(required=False, allow_none=True,
                  validate=validate.Length(max=50), load_default='')
    slug = String(required=False, allow_none=True,
                  validate=validate.Length(max=50), load_default='')
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)


class BrandIn(BaseSchema):
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


class BrandInCreate(BrandIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Brand(**data)


class BrandInUpdate(BrandIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Brand(**data)


class BrandOut(BaseSchema):
    id = Integer()
    name = String()
    slug = String()
    status = String()
    created_at = DateTime()
    updated_at = DateTime()


class BrandsOut(Schema):
    items = List(Nested(BrandOut))
    total = Integer()
