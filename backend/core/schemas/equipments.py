from apiflask import Schema
from apiflask.fields import Boolean, DateTime, Integer, List, Nested, String
from marshmallow import ValidationError, post_load, pre_load, validates_schema, validate
from core.models import Equipment
from core.schemas.utils import BaseSchema, SortBy
from flask_babel import gettext


class EquipmentSearch(Schema):
    equipment_id = Integer(required=False, allow_none=True,
                           data_key='equipmentId', load_default=None)
    brand_id = Integer(
        required=False, allow_none=True, data_key='brandId', load_default=None)
    category_id = Integer(
        required=False, allow_none=True, data_key='categoryId', load_default=None)
    model = String(required=False, allow_none=True,
                   validate=validate.Length(max=50), load_default='')
    reference = String(required=False, allow_none=True,
                       validate=validate.Length(max=50), load_default='')
    model_reference = String(required=False, allow_none=True, data_key='modelReference',
                             validate=validate.Length(max=150), load_default='')
    with_picture = Boolean(required=False, allow_none=True, load_default=False)
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)


class EquipmentIn(BaseSchema):
    id = Integer()
    model = String(required=True, allow_none=False,
                   validate=validate.Length(max=50))
    reference = String(
        required=True, allow_none=False, validate=validate.Length(max=50))
    brand_id = Integer(data_key='brandId')
    category_id = Integer(data_key='categoryId')
    status = String(load_default='ACTIVE')

    @validates_schema
    def model_exists(self, data, **kwargs):
        '''
        Validate the model exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'model' in data:
            raise ValidationError({'message':  gettext('modelRequired')})

        if not data['model']:
            raise ValidationError({'message':  gettext('modelRequired')})

    @validates_schema
    def reference_exists(self, data, **kwargs):
        '''
        Validate the reference exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'reference' in data:
            raise ValidationError({'message':  gettext('referenceRequired')})

        if not data['reference']:
            raise ValidationError({'message':  gettext('referenceRequired')})


class EquipmentInCreate(EquipmentIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Equipment(**data)


class EquipmentInUpdate(EquipmentIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Equipment(**data)


class EquipmentsExistingIn(BaseSchema):
    search = String(required=False, allow_none=True, load_default='')
    equipment_id = Integer(
        required=False, allow_none=True, data_key='equipmentId')

    @pre_load
    def validate_equipment_id(self, data: dict, **kwargs):
        '''Remove equipmentId key if equipmentId its None or ""'''

        if 'equipmentId' in data and not data['equipmentId']:
            data.pop('equipmentId', None)

        return data


class EquipmentOut(BaseSchema):
    id = Integer()
    brand_id = Integer(data_key='brandId')
    brand_name = String(data_key='brandName')
    category_id = Integer(data_key='categoryId')
    category_name = String(data_key='categoryName')
    model_reference = String(data_key='modelReference')
    model = String()
    reference = String()
    main_picture = String(data_key='mainPicture')
    status = String()
    created_at = DateTime(data_key='createdAt')
    updated_at = DateTime(data_key='updatedAt')


class EquipmentsOut(Schema):
    items = List(Nested(EquipmentOut))
    total = Integer()
