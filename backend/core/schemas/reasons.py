from apiflask import Schema
from apiflask.fields import Integer, String, DateTime, List, Nested
from sqlalchemy import and_
from core.models import Reason
from core.schemas.utils import BaseSchema, SortBy
from marshmallow import validate, ValidationError, validates_schema
from flask_babel import gettext
from core.app import db


class ReasonsSearch(BaseSchema):
    category_id = Integer(required=False, allow_none=True,
                          load_default=None, data_key='categoryId')
    name = String(required=False, validate=validate.Length(
        max=100), load_default=None)
    slug = String(required=False, validate=validate.Length(
        max=100), load_default=None)
    description = String(required=False, validate=validate.Length(
        max=100), load_default=None)
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)


class ReasonIn(BaseSchema):
    category_id = Integer(required=True, allow_none=False,
                          data_key='categoryId')
    name = String(required=True, allow_none=False,
                  validate=validate.Length(max=100))
    slug = String(required=True, allow_none=False,
                  validate=validate.Length(max=100))
    description = String(validate=validate.Length(max=100))
    status = String(load_default='ACTIVE')


class ReasonInCreate(ReasonIn):
    @validates_schema
    def check_slug_exists(self, data: dict, **kwargs):
        '''Check if slug exists'''

        slug_exist = db.session.query(Reason)\
            .filter(and_(
                Reason.category_id == data['category_id'],
                Reason.slug == data['slug']))\
            .first()

        if slug_exist:
            raise ValidationError({'message':  gettext('reasonSlugExist')})


class ReasonInUpdate(ReasonIn):
    id = Integer(required=True, allow_none=False)

    @validates_schema
    def check_slug_exists(self, data: dict, **kwargs):
        '''Check if slug exists'''

        current_reason: Reason = db.session.query(
            Reason).filter(Reason.id == data['id']).first()

        if current_reason.slug == data['slug']:
            return data

        slug_exist = db.session.query(Reason)\
            .filter(and_(
                Reason.category_id == data['category_id'],
                Reason.slug == data['slug']))\
            .first()
        if slug_exist:
            raise ValidationError({'message':  gettext('reasonSlugExist')})


class ReasonOut(BaseSchema):
    id = Integer()
    category_id = Integer(data_key='categoryId')
    name = String()
    slug = String()
    description = String()
    status = String()
    created_at = DateTime()
    updated_at = DateTime()


class ReasonsOut(Schema):
    items = List(Nested(ReasonOut))
    total = Integer()
