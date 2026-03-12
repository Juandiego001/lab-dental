from apiflask import Schema
from apiflask.fields import Integer, String, Nested
from marshmallow import EXCLUDE


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class SortBy(Schema):
    key = String()
    order = String()


class Pagination(Schema):
    search = String(load_default='')
    page = Integer()
    per_page = Integer(data_key='perPage')
    sort_by = Nested(SortBy, data_key='sortBy', allow_none=True, load_default=None)


class Message(Schema):
    message = String()
