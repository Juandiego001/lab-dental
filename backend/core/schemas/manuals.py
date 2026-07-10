from marshmallow import validate
from core.utils import format_file_size
from core.schemas.utils import BaseSchema, SortBy
from apiflask.fields import List, Nested, String, Integer, File, Function


class ManualsSearch(BaseSchema):
    equipment_id = Integer(required=False, allow_none=True,
                           load_default=None, data_key='equipmentId')
    title = String(required=False, validate=validate.Length(
        max=50), load_default=None)
    description = String(required=False, validate=validate.Length(
        max=800), load_default=None)
    manual_type_id = Integer(required=False, allow_none=True,
                            load_default=None, data_key='manualTypeId')
    original_name = String(required=False, validate=validate.Length(
        max=100), load_default=None, data_key='originalName')
    extension = String(required=False, validate=validate.Length(
        max=20), load_default=None)
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)


class ManualsIn(BaseSchema):
    equipment_id = Integer(required=True, data_key='equipmentId')
    title = String(required=False, validate=validate.Length(
        max=50), load_default=None)
    description = String(required=False, validate=validate.Length(
        max=800), load_default=None)
    manual_type_id = Integer(required=True, data_key='manualTypeId')


class ManualsCreateIn(ManualsIn):
    file = File(required=True)


class ManualFileOut(BaseSchema):
    original_name = String(data_key='originalName')
    size = Function(lambda data: format_file_size(data.size))
    extension = String()
    path = String()


class ManualTypeOut(BaseSchema):
    id = Integer()
    name = String()
    slug = String()


class ManualOut(BaseSchema):
    id = Integer()
    title = String()
    description = String()
    manual_type_id = Integer(data_key='manualTypeId')
    manual_file = Nested(ManualFileOut, data_key='manualFile')
    manual_type = Nested(ManualTypeOut, data_key='manualType')


class ManualsOut(BaseSchema):
    items = List(Nested(ManualOut))
    total = Integer()


class ManualTypesSearch(BaseSchema):
    name = String(required=False, validate=validate.Length(
        max=100), load_default=None)
    slug = String(required=False, validate=validate.Length(
        max=100), load_default=None)
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)


class ManualTypesOut(BaseSchema):
    items = List(Nested(ManualTypeOut))
    total = Integer()
