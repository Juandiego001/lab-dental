from datetime import datetime
from typing import Literal
from apiflask import Schema, fields
from marshmallow import ValidationError, validates_schema, validate
from core.models import Installation
from core.schemas.utils import BaseSchema


class InstallationSearch(Schema):
    equipment_id = fields.Integer(required=False, allow_none=True, data_key='equipmentId', load_default=None)
    distributor_id = fields.Integer(
        required=False, allow_none=True, data_key='distributorId', load_default=None)
    client_id = fields.Integer(
        required=False, allow_none=True, data_key='clientId', load_default=None)
    serial = fields.String(required=False, allow_none=True,
                          validate=validate.Length(max=50), load_default='')
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(data_key='perPage', load_default=15)


class InstallationIn(BaseSchema):
    id = fields.Integer()
    equipment_id = fields.Integer(data_key='equipmentId')
    client_id = fields.Integer(data_key='clientId')
    site_client_id = fields.Integer(data_key='siteClientId')
    distributor_id = fields.Integer(data_key='distributorId', required=False)
    site_distributor_id = fields.Integer(data_key='siteDistributorId')
    serial = fields.String(required=True, allow_none=False, data_key='serial', validate=validate.Length(max=30))
    installed_date = fields.String(required=True, allow_none=False, data_key='installedDate')
    serial_picture = fields.File(data_key='serialPicture')
    installation_pictures = fields.List(
        fields.File(), data_key='installationPictures')
    status = fields.String(load_default='ACTIVE')

    @validates_schema
    def serial_exists(self, data, **kwargs):
        '''
        Validate the serial exists and have a value
        
        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'serial' in data :
            raise ValidationError({'message':  'Serial required'})
        
        if not data['serial']:
            raise ValidationError({'message':  'Serial required'})

    @validates_schema
    def installed_date_exists(self, data, **kwargs):
        '''
        Validate the installed date exists and have a value
        
        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'installed_date' in data :
            raise ValidationError({'message':  'Installed date required'})
        
        if not data['installed_date']:
            raise ValidationError({'message':  'Installed date required'})


class InstallationInCreate(InstallationIn):
    pass


class InstallationInUpdate(InstallationIn):
    pass


class FileOut(BaseSchema):
    name = fields.String()
    path = fields.String()


def process_expiration_date(row: Installation):
    '''
    Process expiration date when returning installations checking for nulls because fields.Function can fail for nulls
    
    :param row: Description
    :type row: str
    '''

    return row.expiration_date.strftime('%B %d, %Y') if row.expiration_date else ''


class InstallationOut(BaseSchema):
    id = fields.Integer()
    equipment_id = fields.Integer(data_key='equipmentId')
    equipment_model_reference = fields.String(
        data_key='equipmentModelReference')
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
    expiration_date = fields.Function(lambda row: process_expiration_date(row), data_key='expirationDate')
    installation_serial_file = fields.Dict(data_key='installationSerialFile')
    installation_evidences_files = fields.List(
        fields.Dict, data_key='installationEvidencesFiles')
    
    status = fields.String()


class InstallationCreatedNotification(BaseSchema):
    id = fields.Integer()
    equipment_model_reference = fields.String(data_key='equipment')
    distributor_name = fields.String(data_key='distributor')
    client_name = fields.String(data_key='client')
    serial = fields.String()
    installed_date = fields.Function(
        lambda row: row.installed_date.strftime('%B %d, %Y'))
    installation_serial_file = fields.Dict(data_key='serial_file')
    installation_evidences_files = fields.List(
        fields.Dict, data_key='evidences_files')



class InstallationApprovedNotification(BaseSchema):
    id = fields.Integer()
    equipment_model_reference = fields.String(data_key='equipment')
    distributor_id = fields.String()
    distributor_name = fields.String(data_key='distributor')
    site_distributor_name = fields.String(data_key='distributor_site')
    client_name = fields.String(data_key='client')
    site_client_name = fields.String(data_key='client_site')
    serial = fields.String()
    installed_date = fields.Function(
        lambda row: row.installed_date.strftime('%B %d, %Y'))


class InstallationsOut(BaseSchema):
    items = fields.List(fields.Nested(InstallationOut))
    total = fields.Integer()


class InstallationRejectCommentsIn(BaseSchema):
    reject_comments = fields.String(data_key='rejectComments')
