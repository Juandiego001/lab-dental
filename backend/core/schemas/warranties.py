from core.models import Warranty
from marshmallow import post_load, validate
from core.schemas.utils import BaseSchema, SortBy
from apiflask.fields import Dict, Float, String, Integer, DateTime, List, Nested, Function


class WarrantySearch(BaseSchema):
    distributor_id = Integer(
        required=False, allow_none=True, data_key='distributorId', load_default=None)
    equipment_id = Integer(
        required=False, allow_none=True, data_key='equipmentId', load_default=None)
    sale_date = DateTime(
        required=False, allow_none=True, data_key='saleDate', load_default=None)
    invoice = String(required=False, allow_none=True, load_default=None)
    status = String(required=False, allow_none=True, load_default=None)
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)


class PartSchema(BaseSchema):
    id = Integer(required=True, allow_none=False)
    part_number = String(required=True, allow_none=False,
                         data_key='partNumber')
    description = String(required=True, allow_none=False)
    invoice_parts = String(
        required=True, allow_none=False, data_key='invoiceParts')
    quantity = Float(required=True, allow_none=False)
    price = Float(required=True, allow_none=False)
    total = Float(required=True, allow_none=False)


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
    parts = List(Nested(PartSchema), required=False,
                 allow_none=True, load_default=None)
    sale_date = String(required=True, allow_none=False, data_key='saleDate')
    invoice = String(required=True, allow_none=False,
                     validate=validate.Length(max=40))
    shipt_to = String(required=True, allow_none=False,
                      validate=validate.Length(max=400), data_key='shiptTo')
    problem = String(required=True, allow_none=False,
                     validate=validate.Length(max=400))
    solution = String(required=True, allow_none=False,
                      validate=validate.Length(max=400))


class WarrantyInCreate(WarrantyIn):
    pass


class WarrantyInUpdate(WarrantyIn):
    pass


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
    received_at = DateTime()
    equipment_model_reference = String(
        data_key='equipmentModelReference')
    distributor_name = String(data_key='distributorName')
    invoice = String()
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
    country = String()


class PartPDF(BaseSchema):
    part_number = String()
    description = String()
    invoice_parts = String()
    quantity = Integer()
    price = Float()
    total = Float()


class WarrantyEquipmentPDF(BaseSchema):
    model = String()
    reference = String()


class WarrantyPDF(BaseSchema):
    distributor = String()
    contact = Nested(WarrantyContactPDF)
    site = Nested(WarrantySitePDF)
    equipment = Nested(WarrantyEquipmentPDF)
    reasons_names = List(String())
    parts = List(Nested(PartPDF))
    received_at = DateTime()
    equipment_model_reference = String()
    distributor_name = String()
    invoice = String()
    sale_date = Function(
        lambda v: v.sale_date.strftime('%B %d, %Y'))
    shipt_to = String()
    problem = String()
    solution = String()
    status = String()
    created_at = DateTime()
    updated_at = DateTime()


class WarrantiesOut(BaseSchema):
    items = List(Nested(WarrantyOut))
    total = Integer()

class WarrantyRejectCommentsIn(BaseSchema):
    reject_comments = String(data_key='rejectComments')