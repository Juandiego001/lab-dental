from apiflask import Schema, fields
from marshmallow import post_load
from core.models import Equipment
from core.schemas.utils import BaseSchema


class EquipmentIn(BaseSchema):
    id = fields.Integer()
    model = fields.String()
    serial = fields.String()
    brand_id = fields.Integer(data_key='brandId')
    category_id = fields.Integer(data_key='categoryId')
    status = fields.String(load_default='ACTIVE')


class EquipmentInCreate(EquipmentIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Equipment(**data)


class EquipmentInUpdate(EquipmentIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Equipment(**data)


class EquipmentOut(BaseSchema):
    id = fields.Integer()
    brand_id = fields.Integer(data_key='brandId')
    brand_name = fields.String(data_key='brandName')
    category_id = fields.Integer(data_key='categoryId')
    category_name = fields.String(data_key='categoryName')
    serial_model = fields.String(data_key='serialModel')
    model = fields.String()
    serial = fields.String()
    status = fields.String()
    created_at = fields.DateTime(data_key='createdAt')
    updated_at = fields.DateTime(data_key='updatedAt')


class EquipmentsOut(Schema):
    items = fields.List(fields.Nested(EquipmentOut))
    total = fields.Integer()
