from datetime import datetime
import json
from flask_babel import gettext
from core.utils import format_file_size, validate_files_size, validate_file_types
from core.schemas.utils import BaseSchema, SortBy
from marshmallow import ValidationError, post_load, validate, validates_schema
from apiflask.fields import File, Float, String, Integer, DateTime, List, Nested, Function


def set_wco(wco_code: int | None, wco_year: int | None):
    '''Set WCO'''

    if not wco_code:
        return ""
    else:
        return f"WCO-{wco_code:04d}-{wco_year}"


class WarrantySearch(BaseSchema):
    distributor_id = Integer(
        required=False, allow_none=True, data_key='distributorId', load_default=None)
    equipment_id = Integer(
        required=False, allow_none=True, data_key='equipmentId', load_default=None)
    wco_code = Integer(required=False, allow_none=True, load_default=None, data_key='wcoCode')
    wco_year = Integer(required=False, allow_none=True, load_default=None, data_key='wcoYear')
    sale_date = DateTime(
        required=False, allow_none=True, data_key='saleDate', load_default=None)
    invoice = String(required=False, allow_none=True, load_default=None)
    serial = String(required=False, allow_none=True, load_default=None)
    status = String(required=False, allow_none=True, load_default=None)
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)


class PartSchema(BaseSchema):
    id = Integer(required=True, allow_none=False)
    part_number = String(required=True, allow_none=False,
                         data_key='partNumber')
    description = String(required=True, allow_none=False)
    quantity = Integer(required=True, allow_none=False)


class WarrantyIn(BaseSchema):
    distributor_id = Integer(
        required=True, allow_none=False, data_key='distributorId')
    site_id = Integer(required=True, allow_none=False, data_key='siteId')
    equipment_id = Integer(
        required=True, allow_none=False, data_key='equipmentId')
    reasons_ids = List(Integer(), required=True, allow_none=False,
                       data_key='reasonsIds')
    contact_id = Integer(
        required=True, allow_none=False, data_key='contactId')
    sale_date = String(required=True, allow_none=False, data_key='saleDate')
    invoice = String(required=True, allow_none=False,
                     validate=validate.Length(max=40))
    serial = String(required=True, allow_none=False,
                     validate=validate.Length(max=100))
    shipt_to = String(required=True, allow_none=False,
                      validate=validate.Length(max=400), data_key='shiptTo')
    problem = String(required=True, allow_none=False,
                     validate=validate.Length(max=400))
    solution = String(required=True, allow_none=False,
                      validate=validate.Length(max=400))


class WarrantyInCreate(WarrantyIn):
    warranty_files = List(File(), data_key='warrantyFiles', required=True)
    parts = String(required=False, allow_none=True, load_default=None)

    @validates_schema
    def validate_files(self, data: dict, **kwargs):
        '''Validate files types and size'''

        allowed_mimetypes = {'video/mp4',
                             'image/jpeg',
                             'image/png',
                             'image/webp',
                             'image/svg+xml'}
        allowed_extensions = {'mp4', 'jpg',
                              'jpeg', 'png', 'pdf', 'webp', 'svg'}

        the_files = data['warranty_files']

        '''File size validation'''
        invalids = validate_files_size(files_list=the_files)
        if invalids:
            invalids = ", ".join(invalids)
            raise ValidationError({
                "message": gettext(u"50MB max file size exceed for: %(invalids)s", invalids=invalids)
            })

        '''File type validation'''
        invalids = validate_file_types(
            allowed_extensions, allowed_mimetypes, the_files)
        if invalids:
            invalids = ", ".join(invalids)
            raise ValidationError({
                "message": gettext(u"Unsupported file formats for: %(invalids)s", invalids=invalids)
            })

    @post_load
    def serialize_parts(self, data: dict, **kwargs):
        '''Serialize and validate parts'''

        try:
            parts_in = json.loads(data['parts'])

            if not parts_in:
                raise ValidationError(
                    {"message": gettext('warrantyMissingParts')})

            data['parts'] = [PartSchema().load(part) for part in parts_in]
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            raise ValidationError(
                {"message": gettext('warrantyInvalidParts')})

        return data


class WarrantyInUpdate(WarrantyIn):
    parts = List(Nested(PartSchema), required=True)


class WarrantyContactOut(BaseSchema):
    id = Integer()
    full_name = String(data_key='fullName')
    email = String()
    position = String()


class WarrantySiteOut(BaseSchema):
    id = Integer()
    address_id = Integer(data_key='addressId')
    name = String()


class WarrantyEquipmentOut(BaseSchema):
    id = Integer()
    category_id = Integer(data_key='categoryId')
    model = String()
    reference = String()
    model_reference = Function(
        lambda v: v['model'] + ' - ' + v['reference'], data_key='modelReference')


class WarrantyOut(BaseSchema):
    id = Integer()
    distributor_id = Integer(data_key='distributorId')

    contact = Nested(WarrantyContactOut)
    site = Nested(WarrantySiteOut)
    equipment = Nested(WarrantyEquipmentOut)

    equipment_id = Integer(data_key='equipmentId')
    user_approval_id = Integer(data_key='userApprovalId')
    reasons_ids = List(Integer(), data_key='reasonsIds')
    parts = List(Nested(PartSchema))
    received_at = DateTime(data_key='receivedAt')
    wco = Function(lambda v: set_wco(v.wco_code, v.wco_year))
    equipment_model_reference = String(
        data_key='equipmentModelReference')
    distributor_name = String(data_key='distributorName')
    invoice = String()
    serial = String()
    sale_date = String(data_key='saleDate')
    shipt_to = String(data_key='shiptTo')
    problem = String()
    solution = String()
    status = String()
    created_at = DateTime()
    updated_at = DateTime()


class WarrantyContactPDF(BaseSchema):
    full_name = String()
    email = String()
    position = String()


class WarrantySitePDF(BaseSchema):
    address = String()
    city = String()
    state = String()
    country = String()


class PartPDF(BaseSchema):
    part_number = String()
    description = String()
    quantity = Integer()


class WarrantyEquipmentPDF(BaseSchema):
    model = String()
    reference = String()


def set_date_string(v: datetime):
    '''Set Date String for PDF'''

    if v:
        return v.strftime('%B %d, %Y at %H:%M')
    else:
        return ""



class WarrantyPDF(BaseSchema):
    distributor = String()
    contact = Nested(WarrantyContactPDF)
    site = Nested(WarrantySitePDF)
    equipment = Nested(WarrantyEquipmentPDF)
    reasons_names = List(String())
    parts = List(Nested(PartPDF))
    equipment_model_reference = String()
    distributor_name = String()
    user = String()
    invoice = String()
    serial = String()
    sale_date = Function(
        lambda v: v.sale_date.strftime('%B %d, %Y'))
    shipt_to = String()
    problem = String()
    solution = String()
    status = String()
    received_at = Function(lambda v: set_date_string(v.received_at))
    approved_at = Function(lambda v: set_date_string(v.approved_at))
    wco = Function(lambda v: set_wco(v.wco_code, v.wco_year))
    created_at = DateTime()
    updated_at = DateTime()


class WarrantiesOut(BaseSchema):
    items = List(Nested(WarrantyOut))
    total = Integer()


class WarrantyRejectCommentsIn(BaseSchema):
    reject_comments = String(data_key='rejectComments')


class WarrantyFilesSearch(BaseSchema):
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


class WarrantyFileIn(BaseSchema):
    title = String(required=False, allow_none=True)
    description = String(required=False, allow_none=True)


class WarrantyFilesIn(BaseSchema):
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

        the_files = data['files']

        '''File size validation'''
        invalids = validate_files_size(files_list=the_files)
        if invalids:
            invalids = ", ".join(invalids)
            raise ValidationError({
                "message": gettext(u"50MB max file size exceed for: %(invalids)s", invalids=invalids)
            })

        '''File type validation'''
        invalids = validate_file_types(
            allowed_extensions, allowed_mimetypes, the_files)
        if invalids:
            invalids = ", ".join(invalids)
            raise ValidationError({
                "message": gettext(u"Unsupported file formats for: %(invalids)s", invalids=invalids)
            })


class WarrantyFileOut(BaseSchema):
    id = Integer()
    title = String()
    description = String()
    original_name = String(data_key='originalName')
    size = Function(lambda data: format_file_size(data.size))
    extension = String()
    path = String()
    sort_order = Integer(data_key='sortOrder')


class WarrantyFilesOut(BaseSchema):
    items = List(Nested(WarrantyFileOut))
    total = Integer()
