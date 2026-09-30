from apiflask import Schema
from core.models import Notification
from flask_babel import gettext
from core.schemas.utils import BaseSchema, SortBy
from apiflask.fields import DateTime, Integer, List, Nested, String, Boolean
from marshmallow import ValidationError, post_load, pre_load, validate, validates_schema


class NotificationSearch(Schema):
    distributor_id = Integer(
        required=False, allow_none=True, data_key='distributorId', load_default=None)
    name = String(required=False, allow_none=True,
                  validate=validate.Length(max=50), load_default='')
    page = Integer(load_default=1)
    per_page = Integer(data_key='perPage', load_default=15)
    sort_by = Nested(SortBy, data_key='sortBy', load_default=None)


class NotificationIn(BaseSchema):
    name = String(required=True, allow_none=False,
                  validate=validate.Length(max=30))
    distributor_id = Integer(
        required=False, allow_none=True, data_key='distributorId')
    users_ids = List(Integer, data_key='usersIds')
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
                {'message':  gettext('notificationNameRequired')})

        if not data['name']:
            raise ValidationError(
                {'message':  gettext('notificationNameRequired')})


class NotificationInCreate(NotificationIn):
    @pre_load
    # Es posible que la notificación sea creada por un distribuidor, por lo tanto no se enviaría distributor_id sino que se tomaría del usuario
    def pop_null_distributor_id(self, data: dict, **kwargs):
        '''Remove null distributor_id'''

        if ('distributor_id' in data and not (data['distributor_id'])):
            data.pop('distributor_id')

        return data

    @post_load
    def make_object(self, data: dict, **kwargs):
        users_ids = data.pop('users_ids')
        return Notification(**data), users_ids


class NotificationInUpdate(NotificationIn):
    id = Integer()

    @pre_load
    # Es posible que el grupo sea creado por un distribuidor, por lo tanto no se enviaría distributor_id sino que se tomaría del usuario
    def pop_null_distributor_id(self, data: dict, **kwargs):
        '''Remove null distributor_id'''

        if ('distributor_id' in data and not (data['distributor_id'])):
            data.pop('distributor_id')

        return data

    @post_load
    def make_object(self, data: dict, **kwargs):
        users_ids = data.pop('users_ids')
        return Notification(**data), users_ids


class NotificationOut(BaseSchema):
    id = Integer()
    name = String()
    distributor_id = Integer(data_key='distributorId')
    distributor_name = String(data_key='distributorName')
    users_ids = List(Integer, data_key='usersIds')
    status = String()
    created_at = DateTime(data_key='createdAt')
    updated_at = DateTime(data_key='updatedAt')


class NotificationsOut(Schema):
    items = List(Nested(NotificationOut))
    total = Integer()


class NotificationModuleIn(BaseSchema):
    id = Integer()
    create = Boolean()
    update = Boolean()
    delete = Boolean()


class NotificationModuleOut(Schema):
    id = Integer()
    create = Boolean()
    update = Boolean()
    delete = Boolean()
    module_name = String(data_key='moduleName')


class NotificationsModulesOut(BaseSchema):
    items = List(Nested(NotificationModuleOut))
    total = Integer()
