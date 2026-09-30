from apiflask import Schema
from apiflask.fields import Integer, List, Nested, String, File, Dict, Function
from marshmallow import ValidationError, validates_schema, validate
from core.models import Installation
from core.schemas.utils import BaseSchema, SortBy
from flask_babel import gettext


class InstallationSearch(Schema):
    equipment_id = Integer(required=False, allow_none=True,
                           data_key='equipmentId', load_default=None)
    distributor_id = Integer(
        required=False, allow_none=True, data_key='distributorId', load_default=None)
    client_id = Integer(
        required=False, allow_none=True, data_key='clientId', load_default=None)
    serial = String(required=False, allow_none=True,
                    validate=validate.Length(max=50), load_default='')
    status = String(required=False, allow_none=True,
                    validate=validate.Length(max=20))
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)


class InstallationIn(BaseSchema):
    id = Integer()
    equipment_id = Integer(data_key='equipmentId')
    client_id = Integer(data_key='clientId')
    site_client_id = Integer(data_key='siteClientId')
    distributor_id = Integer(data_key='distributorId', required=False)
    site_distributor_id = Integer(data_key='siteDistributorId')
    serial = String(required=True, allow_none=False,
                    data_key='serial', validate=validate.Length(max=30))
    installed_date = String(
        required=True, allow_none=False, data_key='installedDate')
    serial_picture = File(data_key='serialPicture')
    installation_pictures = List(
        File(), data_key='installationPictures')
    status = String(load_default='ACTIVE')

    @validates_schema
    def serial_exists(self, data, **kwargs):
        '''
        Validate the serial exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'serial' in data:
            raise ValidationError({'message':  gettext('serialRequired')})

        if not data['serial']:
            raise ValidationError({'message':  gettext('serialRequired')})

    @validates_schema
    def installed_date_exists(self, data, **kwargs):
        '''
        Validate the installed date exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'installed_date' in data:
            raise ValidationError(
                {'message':  gettext('installedDateRequired')})

        if not data['installed_date']:
            raise ValidationError({'message':  gettext('serialRequired')})


class InstallationInCreate(InstallationIn):
    pass


class InstallationInUpdate(InstallationIn):
    pass


def process_expiration_date(row: Installation):
    '''
    Process expiration date when returning installations checking for nulls because Function can fail for nulls

    :param row: Description
    :type row: str
    '''

    return row.expiration_date.strftime('%B %d, %Y') if row.expiration_date else ''


class InstallationFileOut(BaseSchema):
    original_name = String(data_key='originalName')
    hash_name = String(data_key='hashName')


class InstallationOut(BaseSchema):
    id = Integer()
    equipment_id = Integer(data_key='equipmentId')
    equipment_model_reference = String(
        data_key='equipmentModelReference')
    distributor_id = Integer(data_key='distributorId')
    distributor_name = String(data_key='distributorName')
    site_distributor_id = Integer(data_key='siteDistributorId')
    site_distributor_name = String(data_key='siteDistributorName')
    client_id = Integer(data_key='clientId')
    client_name = String(data_key='clientName')
    site_client_id = Integer(data_key='siteClientId')
    site_client_name = String(data_key='siteClientName')
    serial = String()
    installed_date = String(data_key='installedDate')
    expiration_date = Function(
        lambda row: process_expiration_date(row), data_key='expirationDate')
    installation_serial_file = Nested(
        InstallationFileOut, data_key='installationSerialFile')
    installation_evidences_files = List(
        Nested(InstallationFileOut), data_key='installationEvidencesFiles')
    status = String()


class InstallationCreatedNotification(BaseSchema):
    id = Integer()
    equipment_model_reference = String(data_key='equipment')
    distributor_name = String(data_key='distributor')
    client_name = String(data_key='client')
    serial = String()
    installed_date = Function(
        lambda row: row.installed_date.strftime('%B %d, %Y'))
    installation_serial_file = Dict(data_key='serial_file')
    installation_evidences_files = List(
        Dict, data_key='evidences_files')


class InstallationApprovedNotification(BaseSchema):
    id = Integer()
    equipment_model_reference = String(data_key='equipment')
    distributor_id = String()
    distributor_name = String(data_key='distributor')
    site_distributor_name = String(data_key='distributor_site')
    client_name = String(data_key='client')
    site_client_name = String(data_key='client_site')
    serial = String()
    installed_date = Function(
        lambda row: row.installed_date.strftime('%B %d, %Y'))


class InstallationsOut(BaseSchema):
    items = List(Nested(InstallationOut))
    total = Integer()


class InstallationRejectCommentsIn(BaseSchema):
    reject_comments = String(data_key='rejectComments')
