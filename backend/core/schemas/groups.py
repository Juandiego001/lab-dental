from apiflask import Schema, fields
from core.schemas.utils import BaseSchema


class GroupIn(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    slug = fields.String()


class GroupInCreate(GroupIn):
    pass


class GroupInUpdate(GroupIn):
    status = fields.String(load_default='ACTIVE')


class GroupOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    slug = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class GroupsOut(Schema):
    items = fields.List(fields.Nested(GroupOut))
    total = fields.Integer()
