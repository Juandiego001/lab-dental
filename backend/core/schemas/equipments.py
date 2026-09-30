from apiflask import Schema
from flask_babel import gettext
from core.utils import format_file_size, validate_file_types
from core.schemas.utils import BaseSchema, SortBy
from marshmallow import ValidationError, validates_schema, validate
from apiflask.fields import Boolean, DateTime, File, Integer, List, Nested, String, Function


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
        '''Remove equipmentId key if equipmentId its None or ""'''

        if 'equipmentId' in data and not data['equipmentId']:
            data.pop('equipmentId', None)

        return data


class EquipmentFilesSearch(BaseSchema):
    title = String(required=False, validate=validate.Length(
        max=50), load_default=None)
    description = String(required=False, validate=validate.Length(
        max=100), load_default=None)
    original_name = String(required=False, validate=validate.Length(
        max=100), load_default=None, data_key='originalName')
    extension = String(required=False, validate=validate.Length(
        max=20), load_default=None)
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)


class EquipmentFileIn(BaseSchema):
    title = String(required=False, allow_none=True)
    description = String(required=False, allow_none=True)


class EquipmentFilesIn(BaseSchema):
    files = List(File(), required=True)

    @validates_schema
    def validate_files_types(self, data: dict, **kwargs):
        '''Validate files types'''

        allowed_mimetypes = {'video/mp4',
                             'image/jpeg',
                             'image/png',
                             'image/webp',
                             'image/svg+xml'}
        allowed_extensions = {'mp4', 'jpg',
                              'jpeg', 'png', 'pdf', 'webp', 'svg'}
        invalids = validate_file_types(
            allowed_extensions, allowed_mimetypes, data['files'])
        if invalids:
            invalids = ", ".join(invalids)
            raise ValidationError({
                "message": gettext(u"Unsupported file formats for: %(invalids)s", invalids=invalids)
            })


class EquipmentFileOut(BaseSchema):
    id = Integer()
    title = String()
    description = String()
    original_name = String(data_key='originalName')
    size = Function(lambda data: format_file_size(data.size))
    hash_name = String(data_key='hashName')
    extension = String()
    sort_order = Integer(data_key='sortOrder')


class EquipmentFilesOut(BaseSchema):
    items = List(Nested(EquipmentFileOut))
    total = Integer()


class EquipmentFileOrderIn(BaseSchema):
    new_sort_order = Integer(data_key='newSortOrder')


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
    extension = String()
    status = String()
    created_at = DateTime(data_key='createdAt')
    updated_at = DateTime(data_key='updatedAt')


class EquipmentsOut(BaseSchema):
    items = List(Nested(EquipmentOut))
    total = Integer()
