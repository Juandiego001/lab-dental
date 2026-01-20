from apiflask import Schema, fields
from core.schemas.utils import BaseSchema


class PartIn(BaseSchema):
    id = fields.Integer()
    serial = fields.String()


class PartInCreate(PartIn):
    pass


class PartInUpdate(PartIn):
    status = fields.String(load_default='ACTIVE')


class PartOut(BaseSchema):
    id = fields.Integer()
    serial = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class PartsOut(Schema):
    items = fields.List(fields.Nested(PartOut))
    total = fields.Integer()
