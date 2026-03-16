from apiflask import Schema
from apiflask.fields import Boolean, DateTime, Dict, File, Integer, List, Nested, String, Function
from marshmallow import ValidationError, post_load, pre_load, validates_schema, validate
from core.models import Equipment
from core.schemas.utils import BaseSchema, SortBy
from flask_babel import gettext
from datetime import datetime


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
    # Para además de traer el equipo, decidir traerlo con imagen
    with_picture = Boolean(data_key='withPicture',
                           required=False, allow_none=True, load_default=False)
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
    main_picture = File(data_key='mainPicture')
    secondary_pictures = List(
        File(), data_key='secondaryPictures')
    videos = List(File())
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
    pass


class EquipmentInUpdate(EquipmentIn):
    pass


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


class EquipmentFileOut(Schema):
    id = Integer()
    original_name = String(data_key='originalName')
    size = String(data_key='size')
    extension = String()
    path = String()
    is_main = String(data_key='isMain')


class EquipmentFilesOut(Schema):
    equipment_files = List(Nested(EquipmentFileOut), data_key='equipmentFiles')
