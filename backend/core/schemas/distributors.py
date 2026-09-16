from core.app import db
from sqlalchemy import and_
from flask_babel import gettext
from core.schemas.utils import BaseSchema, SortBy
from marshmallow import pre_load, validates_schema, ValidationError, validate
from apiflask.fields import Boolean, DateTime, Dict, Function, String, List, Integer, Nested, File
from core.models import Brand, Contact, Distributor, DistributorAligner, DistributorEmail, DistributorPhone
from core.services.distributors import aligner_exist
from core.utils import validate_empty_files, validate_file_types, validate_files_size


class DistributorSearch(BaseSchema):
    distributors_ids = List(Integer(required=False, allow_none=True, load_default=None),
                            required=False, allow_none=True, data_key='distributorsIds', load_default=None)
    name = String(required=False, allow_none=True,
                  validate=validate.Length(max=50), load_default='')
    bp = String(required=False, allow_none=True,
                validate=validate.Length(max=50), load_default='')
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)

    @validates_schema
    def validate_distributors_ids(self, data: dict, **kwargs):
        '''
        Docstring for validate_distributors_ids

        :param self: Description
        :param data: Description
        :type data: dict
        :param kwargs: Description
        '''

        if not 'distributors_ids' in data:
            return data

        if not data['distributors_ids']:
            return data

        for i in data['distributors_ids']:
            if i != None:
                return data

        data['distributors_ids'] = None
        return data


class DistributorEmailSchema(BaseSchema):
    id = Integer(required=False, allow_none=False)
    email = String()
    status = String()


class DistributorPhoneSchema(BaseSchema):
    id = Integer(required=False, allow_none=False)
    phone = String()
    status = String()


class DistributorIn(BaseSchema):
    name = String(required=True, allow_none=False,
                  validate=validate.Length(max=50))
    bp = String(required=True, allow_none=False,
                validate=validate.Length(max=50))
    brands_ids = List(Integer, data_key='brandsIds', required=False,
                      allow_none=True, load_default=[])
    emails = List(Nested(DistributorEmailSchema), required=False,
                  allow_none=True, load_default=[])
    phones = List(Nested(DistributorPhoneSchema), required=False,
                  allow_none=True, load_default=[])
    notes = String(required=False, allow_none=True,
                   validate=validate.Length(max=200), load_default=None)
    status = String(load_default='ACTIVE')

    @validates_schema
    def name_exists(self, data, **kwargs):
        '''
        Validate the name exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'name' in data:
            raise ValidationError(
                {'message':  gettext('distributorNameRequired')})

        if not data['name']:
            raise ValidationError(
                {'message':  gettext('distributorNameRequired')})

    @validates_schema
    def bp_exists(self, data, **kwargs):
        '''
        Validate the BP Number exists and have a value

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'bp' in data:
            raise ValidationError(
                {'message':  gettext('distributorBpRequired')})

        if not data['bp']:
            raise ValidationError(
                {'message':  gettext('distributorBpRequired')})

    @validates_schema
    def brands_exists(self, data, **kwargs):
        '''Validate the brands exists'''

        if not 'brands_ids' in data:
            raise ValidationError(
                {'message':  gettext('brandRequired')})

        if not data['brands_ids']:
            raise ValidationError(
                {'message':  gettext('brandRequired')})

        for brand_id in data['brands_ids']:
            the_brand = db.session.query(Brand)\
                .filter(Brand.id == brand_id, Brand.status == 'ACTIVE')\
                .first()
            if not the_brand:
                raise ValidationError(
                    {'message':  gettext('brandDoesntExist')})

    @validates_schema
    def emails_exists(self, data, **kwargs):
        '''Validate emails exists and have max length'''

        if not 'emails' in data:
            return data

        emails_list = []
        for email_obj in data['emails']:
            if email_obj['status'] == 'INACTIVE' or 'id' in email_obj:
                continue

            if len(email_obj['email']) > 150:
                raise ValidationError(
                    {'message':  gettext('distributorEmailLengthExceededError')})

            emails_list.append(email_obj['email'])

        emails_exists = db.session.query(DistributorEmail)\
            .filter(
                and_(
                    DistributorEmail.email.in_(emails_list),
                    DistributorEmail.status == 'ACTIVE')
        )\
            .all()

        if emails_exists:
            raise ValidationError(
                {'message':  gettext('distributorEmailExistsError')})

    @validates_schema
    def phones_exists(self, data, **kwargs):
        '''Validate phones exists and have max length'''

        if not 'phones' in data:
            return data

        phones_list = []
        for phone_obj in data['phones']:
            if phone_obj['status'] == 'INACTIVE' or 'id' in phone_obj:
                continue

            if len(phone_obj['phone']) > 20:
                raise ValidationError(
                    {'message':  gettext('distributorPhoneLengthExceededError')})

            phones_list.append(phone_obj['phone'])

        phones_exists = db.session.query(DistributorPhone)\
            .filter(and_(DistributorPhone.phone.in_(phones_list), DistributorPhone.status == 'ACTIVE'))\
            .all()

        if phones_exists:
            raise ValidationError(
                {'message':  gettext('distributorPhoneExistsError')})


class DistributorInCreate(DistributorIn):

    @validates_schema
    def name_already_exists(self, data, **kwargs):
        '''
        Validate the name exists in other distributor

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        distributor_exists = db.session.query(Distributor)\
            .filter(Distributor.name == data['name'])\
            .first()
        if distributor_exists:
            raise ValidationError(
                {'message':  gettext('distributorNameExistsError')})

    @validates_schema
    def bp_already_exists(self, data, **kwargs):
        '''
        Validate the BP Number exists in other distributor

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        distributor_exists = db.session.query(Distributor)\
            .filter(Distributor.bp == data['bp'])\
            .first()
        if distributor_exists:
            raise ValidationError(
                {'message':  gettext('distributorBPExistsError')})


class DistributorInUpdate(DistributorIn):
    id = Integer(required=True, allow_none=False)

    @pre_load
    def set_distributor_object(self, data, **kwargs):
        '''Get distributor object'''

        distributor = db.session.query(Distributor).filter(
            Distributor.id == data['id']).first()

        if not distributor:
            raise ValidationError(
                {'message': gettext('distributorDoesntExist')}
            )

        self.distributor_obj = distributor
        return data

    @validates_schema
    def name_already_exists(self, data, **kwargs):
        '''
        Validate the name exists in other distributor

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        the_distributor: Distributor = self.distributor_obj

        # If the name did not change, keep going - do not need to do a validation
        if the_distributor.name == data['name']:
            return data

        distributor_exists = db.session.query(Distributor)\
            .filter(Distributor.name == data['name'])\
            .first()

        if distributor_exists:
            raise ValidationError(
                {'message':  gettext('distributorNameExistsError')})

    @validates_schema
    def bp_already_exists(self, data, **kwargs):
        '''
        Validate the BP Number exists in other distributor

        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        the_distributor: Distributor = self.distributor_obj

        # If the BP Number did not change, keep going - do not need to do a validation
        if the_distributor.bp == data['bp']:
            return data

        distributor_exists = db.session.query(Distributor)\
            .filter(Distributor.bp == data['bp'])\
            .first()
        if distributor_exists:
            raise ValidationError(
                {'message':  gettext('distributorBPExistsError')})


def get_brands_ids(d: Distributor):
    '''Process distributors_brands list object and return only the ids'''

    if not d.distributors_brands:
        return []

    return [distributor_brand.brand_id for distributor_brand in d.distributors_brands]


def get_brands(d: Distributor):
    '''Process distributors_brands list object and return only the brands names'''

    if not d.distributors_brands:
        return []

    return [distributor_brand.brand.name for distributor_brand in d.distributors_brands]


class DistributorOut(BaseSchema):
    id = Integer()
    name = String()
    bp = String()
    notes = String()
    brands_ids = Function(lambda d: get_brands_ids(d), data_key='brandsIds')
    brands = Function(lambda d: get_brands(d))
    distributors_emails = List(
        Nested(DistributorEmailSchema), data_key='emails')
    distributors_phones = List(
        Nested(DistributorPhoneSchema), data_key='phones')
    status = String()
    created_at = DateTime(data_key='createdAt')
    updated_at = DateTime(data_key='updatedAt')


class DistributorsOut(BaseSchema):
    items = List(Nested(DistributorOut))
    total = Integer()


class DistributorsExistingIn(BaseSchema):
    search = String(required=False)
    distributors_ids = List(Integer(
    ), required=False, allow_none=True, load_default=[], data_key='distributorsIds')

    @validates_schema
    def validate_distributors_ids(self, data, **kwargs):
        if 'distributors_ids' in data and not data['distributors_ids']:
            data['distributors_ids'] = []

        return data


class ContactSearch(BaseSchema):
    distributor_id = Integer(
        required=True, allow_none=False, data_key='distributorId')
    contacts_ids = List(
        Integer(), required=False,
        allow_none=True, load_default=None, data_key='contactsIds')
    full_name = String(required=False, allow_none=True,
                       validate=validate.Length(max=50), load_default='', data_key='fullName')
    email = String(required=False, allow_none=True,
                   validate=validate.Length(max=150), load_default='')
    phone = String(required=False, allow_none=True,
                   validate=validate.Length(max=20), load_default='')
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)


class ContactOut(BaseSchema):
    id = Integer()
    full_name = String(data_key='fullName')
    email = String()
    phone = String()
    position = String()


class ContactsOut(BaseSchema):
    items = List(Nested(ContactOut))
    total = Integer()


class ContactIn(BaseSchema):
    distributor_id = Integer(
        required=True, allow_none=False, data_key='distributorId')
    id = Integer(required=False)
    full_name = String(
        required=True,
        allow_none=False,
        validate=validate.Length(max=50),
        data_key='fullName'
    )
    email = String(required=False, validate=validate.Length(max=150))
    phone = String(required=False, validate=validate.Length(max=20))
    position = String(required=False, validate=validate.Length(max=150))


class ContactInCreate(ContactIn):
    @validates_schema
    def email_exists(self, data, **kwargs):
        '''Validate email exists and have max length'''

        if not 'email' in data:
            return data

        email_exists = db.session.query(Contact)\
            .filter(
                and_(
                    Contact.email == data['email'],
                    Contact.status == 'ACTIVE')
        )\
            .first()

        if email_exists:
            raise ValidationError(
                {'message':  gettext('contactEmailExistsError')})


class AlignerAllOut(BaseSchema):
    id = Integer()
    version = Dict()
    serialNumber = String(data_key='serial')
    specs = Dict()
    specsExpiration = Dict()
    connected = Boolean()
    createdAt = String()


class AlignersAllOut(BaseSchema):
    items = List(Nested(AlignerAllOut))


class AlignerInCreate(BaseSchema):
    distributor_id = Integer(
        required=True, allow_none=False, data_key='distributorId')
    serial = String(required=True, allow_none=False)

    @validates_schema
    def serial_exist(self, data, **kwargs):
        '''Validate if serial exist'''

        if not aligner_exist(data['serial']):
            raise ValidationError({'message': gettext('alignerNotFound')})

    @validates_schema
    def serial_already_exist(self, data, **kwargs):
        '''Validate if serial already exists in the distributor'''

        if db.session.query(DistributorAligner)\
            .filter(DistributorAligner.serial == data['serial'])\
                .first():
            raise ValidationError(
                {'message': gettext('alignerAlreadyAssociated')})


class AlignerFileIn(BaseSchema):
    file = File(required=True)

    @validates_schema
    def valid_file(self, data, **kwargs):
        '''Validate Plain Text File'''

        allowed_mimetypes = {'text/plain'}
        allowed_extensions = {'txt'}

        the_file = data['file']

        '''Empty files validation'''
        invalids = validate_empty_files(files_list=[the_file])
        if invalids:
            invalids = ", ".join(invalids)
            raise ValidationError({
                "message": gettext(u"Invalid empty files: %(invalids)s", invalids=invalids)
            })

        '''File size validation'''
        invalids = validate_files_size(files_list=[the_file], max_size_mb=10)
        if invalids:
            invalids = ", ".join(invalids)
            raise ValidationError({
                "message": gettext(u"10MB max file size exceed for: %(invalids)s", invalids=invalids)
            })

        '''File type validation'''
        invalids = validate_file_types(
            allowed_extensions, allowed_mimetypes, [the_file])
        if invalids:
            invalids = ", ".join(invalids)
            raise ValidationError({
                "message": gettext(u"Unsupported file formats for: %(invalids)s", invalids=invalids)
            })


class AlignerValidation(BaseSchema):
    serial = String()
    message_type = String(data_key='messageType')
    message = String()


class AlignersValidationsOut(BaseSchema):
    validations = List(Nested(AlignerValidation))


class AlignersMultipleIn(BaseSchema):
    serials = List(Nested(AlignerValidation))


class AlignerAliasIn(BaseSchema):
    alias = String(required=True, allow_none=False, validate=validate.Length(max=30))
