from apiflask import Schema, fields
from core.schemas.utils import BaseSchema


class ReasonIn(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    slug = fields.String()


class ReasonInCreate(ReasonIn):
    pass


class ReasonInUpdate(ReasonIn):
    status = fields.String(load_default='ACTIVE')


class ReasonOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    slug = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class ReasonsOut(Schema):
    items = fields.List(fields.Nested(ReasonOut))
