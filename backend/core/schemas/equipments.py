from apiflask import Schema, fields
from marshmallow import ValidationError, post_load, pre_load, validates_schema, validate
from core.models import Equipment
from core.schemas.utils import BaseSchema


class EquipmentSearch(Schema):
    equipment_id = fields.Integer(required=False, allow_none=True, data_key='equipmentId', load_default=None)
    brand_id = fields.Integer(
        required=False, allow_none=True, data_key='brandId', load_default=None)
    category_id = fields.Integer(
        required=False, allow_none=True, data_key='categoryId', load_default=None)
    model = fields.String(required=False, allow_none=True,
                          validate=validate.Length(max=50), load_default='')
    reference = fields.String(required=False, allow_none=True,
                              validate=validate.Length(max=50), load_default='')
    with_picture = fields.Boolean(required=False, allow_none=True, load_default=False)
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(data_key='perPage', load_default=15)


class EquipmentIn(BaseSchema):
    id = fields.Integer()
    model = fields.String(required=True, allow_none=False,
                          validate=validate.Length(max=50))
    reference = fields.String(
        required=True, allow_none=False, validate=validate.Length(max=50))
    brand_id = fields.Integer(data_key='brandId')
    category_id = fields.Integer(data_key='categoryId')
    status = fields.String(load_default='ACTIVE')

    @validates_schema
    def model_exists(self, data, **kwargs):
        '''
        Validate the model exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'model' in data:
            raise ValidationError({'message':  'Model required'})

        if not data['model']:
            raise ValidationError({'message':  'Model required'})

    @validates_schema
    def reference_exists(self, data, **kwargs):
        '''
        Validate the reference exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'reference' in data:
            raise ValidationError({'message':  'Reference required'})

        if not data['reference']:
            raise ValidationError({'message':  'Reference required'})


class EquipmentInCreate(EquipmentIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Equipment(**data)


class EquipmentInUpdate(EquipmentIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Equipment(**data)


class EquipmentsExistingIn(BaseSchema):
    search = fields.String(required=False, allow_none=True, load_default='')
    equipment_id = fields.Integer(
        required=False, allow_none=True, data_key='equipmentId')

    @pre_load
    def validate_equipment_id(self, data: dict, **kwargs):
        '''Remove equipmentId key if equipmentId its None or ""'''

        if 'equipmentId' in data and not data['equipmentId']:
            data.pop('equipmentId', None)

        return data


class EquipmentOut(BaseSchema):
    id = fields.Integer()
    brand_id = fields.Integer(data_key='brandId')
    brand_name = fields.String(data_key='brandName')
    category_id = fields.Integer(data_key='categoryId')
    category_name = fields.String(data_key='categoryName')
    model_reference = fields.String(data_key='modelReference')
    model = fields.String()
    reference = fields.String()
    main_picture = fields.String(data_key='mainPicture')
    status = fields.String()
    created_at = fields.DateTime(data_key='createdAt')
    updated_at = fields.DateTime(data_key='updatedAt')


class EquipmentsOut(Schema):
    items = fields.List(fields.Nested(EquipmentOut))
    total = fields.Integer()
