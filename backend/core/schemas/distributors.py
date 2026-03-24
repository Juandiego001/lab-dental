from sqlalchemy import and_
from core.app import db
from core.models import Contact, DistributorEmail, DistributorPhone
from apiflask import Schema
from apiflask.fields import DateTime, String, List, Integer, Nested
from marshmallow import validates_schema, ValidationError, validate
from core.schemas.utils import BaseSchema, SortBy
from flask_babel import gettext


class DistributorSearch(Schema):
    distributors_ids = List(Integer(required=False, allow_none=True, load_default=None),
                            required=False, allow_none=True, data_key='distributorsIds', load_default=None)
    name = String(required=False, allow_none=True,
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


class DistributorEmailSchema(Schema):
    id = Integer(required=False, allow_none=False)
    email = String()
    status = String()


class DistributorPhoneSchema(Schema):
    id = Integer(required=False, allow_none=False)
    phone = String()
    status = String()


class DistributorIn(BaseSchema):
    id = Integer()
    name = String(required=True, allow_none=False,
                  validate=validate.Length(max=50))
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


class DistributorOut(BaseSchema):
    id = Integer()
    name = String()
    notes = String()
    distributors_emails = List(
        Nested(DistributorEmailSchema), data_key='emails')
    distributors_phones = List(
        Nested(DistributorPhoneSchema), data_key='phones')
    status = String()
    created_at = DateTime(data_key='createdAt')
    updated_at = DateTime(data_key='updatedAt')


class DistributorsOut(Schema):
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
