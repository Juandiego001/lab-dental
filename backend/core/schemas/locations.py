from apiflask import Schema, fields
from core.schemas.utils import BaseSchema


class LocationSearch(Schema):
    id = fields.Integer(required=False, allow_none=True, load_default=None)
    name = fields.String(required=False, allow_none=True, load_default='')
    page = fields.Integer()
    per_page = fields.Integer(data_key='perPage')


class LocationOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()


class LocationsOut(Schema):
    items = fields.List(fields.Nested(LocationOut))
