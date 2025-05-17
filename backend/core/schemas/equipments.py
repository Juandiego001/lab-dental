from apiflask import Schema, fields
from core.schemas.utils import BaseSchema


class EquipmentIn(BaseSchema):
    id = fields.Integer()
    model = fields.String()
    serial = fields.String()


class EquipmentInCreate(EquipmentIn):
    pass


class EquipmentInUpdate(EquipmentIn):
    status = fields.String(load_default='ACTIVE')


class EquipmentOut(BaseSchema):
    id = fields.Integer()
    model = fields.String()
    serial = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class EquipmentsOut(Schema):
    items = fields.List(fields.Nested(EquipmentOut))
