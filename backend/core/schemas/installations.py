from datetime import datetime
from apiflask import Schema, fields
from core.schemas.utils import BaseSchema


class InstallationIn(BaseSchema):
    id = fields.Integer()
    equipment_id = fields.Integer(data_key='equipmentId')
    client_id = fields.Integer(data_key='clientId')
    site_client_id = fields.Integer(data_key='siteClientId')
    distributor_id = fields.Integer(data_key='distributorId', required=False)
    site_distributor_id = fields.Integer(data_key='siteDistributorId')
    serial = fields.String(data_key='serial')
    installed_date = fields.String(data_key='installedDate')
    serial_picture = fields.File(data_key='serialPicture')
    installation_pictures = fields.List(
        fields.File(), data_key='installationPictures')
    status = fields.String(load_default='ACTIVE')


class InstallationInCreate(InstallationIn):
    pass


class InstallationInUpdate(InstallationIn):
    pass


class FileOut(BaseSchema):
    name = fields.String()
    path = fields.String()


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
    serial = fields.String(data_key='serial')
    installed_date = fields.String(data_key='installedDate')
    installation_serial_file = fields.Dict(data_key='installationSerialFile')
    installation_evidences_files = fields.List(fields.Dict, data_key='installationEvidencesFiles')
    status = fields.String()


class InstallationCreatedNotification(BaseSchema):
    id = fields.Integer()
    equipment_serial_model = fields.String(data_key='equipment')
    distributor_name = fields.String(data_key='distributor')
    client_name = fields.String(data_key='client')
    serial = fields.String()
    installed_date = fields.Function(lambda row: row.installed_date.strftime('%B %d, %Y'))
    installation_serial_file = fields.Dict(data_key='serial_file')
    installation_evidences_files = fields.List(fields.Dict, data_key='evidences_files')


class InstallationApprovedNotification(BaseSchema):
    id = fields.Integer()
    equipment_serial_model = fields.String(data_key='equipment')
    distributor_id = fields.String()
    distributor_name = fields.String(data_key='distributor')
    site_distributor_name = fields.String(data_key='distributor_site')
    client_name = fields.String(data_key='client')
    site_client_name = fields.String(data_key='client_site')
    serial = fields.String()
    installed_date = fields.Function(lambda row: row.installed_date.strftime('%B %d, %Y'))


class InstallationsOut(BaseSchema):
    items = fields.List(fields.Nested(InstallationOut))
    total = fields.Integer()


class InstallationRejectCommentsIn(BaseSchema):
    reject_comments = fields.String(data_key='rejectComments')