from bcrypt import hashpw, gensalt
from core.models import Installation
from apiflask import Schema, fields
from marshmallow import post_load, pre_load
from core.schemas.utils import BaseSchema


class InstallationIn(BaseSchema):
    id = fields.Integer()
    equipment_id = fields.Integer(data_key='equipmentId')
    client_id = fields.Integer(data_key='clientId')
    site_client_id = fields.Integer(data_key='siteClientId')
    distributor_id = fields.Integer(data_key='distributorId', required=False)
    site_distributor_id = fields.Integer(data_key='siteDistributorId')
    installed_date = fields.String(data_key='installedDate')
    format_picture = fields.File(data_key='formatPicture')
    serial_picture = fields.File(data_key='serialPicture')
    installation_pictures = fields.List(fields.File(), data_key='installationPictures')
    status = fields.String(load_default='ACTIVE')


class InstallationInCreate(InstallationIn):
    pass


class InstallationInUpdate(InstallationIn):
    @post_load
    def make_object(self, data, **kwargs):
        return Installation(**data)


class InstallationOut(BaseSchema):
    id = fields.Integer()
    equipment_id = fields.Integer(data_key='equipmentId')
    equipment_serial_model = fields.String(data_key='equipmentSerialModel')
    distributor_id = fields.Integer(data_key='distributorId')
    distributor_name = fields.String(data_key='distributorName')
    site_distributor_id = fields.Integer(data_key='siteDistributorId')
    site_distributor_name = fields.String(data_key='siteDistributorName')
    client_id = fields.Integer(data_key='clientId')
    client_name = fields.String(data_key='clientName')
    site_client_id = fields.Integer(data_key='siteClientId')
    site_client_name = fields.String(data_key='siteClientName')
    installed_date = fields.String(data_key='installedDate')
    format_picture = fields.File(date_key='formatPicture')
    serial_picture = fields.File(date_key='serialPicture')
    installation_pictures = fields.File(date_key='installationPictures')
    status = fields.String()


class InstallationsOut(Schema):
    items = fields.List(fields.Nested(InstallationOut))
    total = fields.Integer()
