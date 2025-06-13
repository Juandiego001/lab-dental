from apiflask import Schema, fields
from core.schemas.utils import BaseSchema


class LocationOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()


class LocationsOut(Schema):
    items = fields.List(fields.Nested(LocationOut))
