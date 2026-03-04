from apiflask import Schema, fields
from marshmallow import ValidationError, validates_schema, validate
from core.schemas.utils import BaseSchema
from flask_babel import gettext


class ListIn(BaseSchema):
    id = fields.Integer()
    name = fields.String(required=True, allow_none=False, validate=validate.Length(max=30))
    distributors_ids = fields.List(fields.Integer, data_key='distributorsIds')
    users_ids = fields.List(fields.Integer, data_key='usersIds', required=False, allow_none=True)
    status = fields.String(load_default='ACTIVE')

    @validates_schema
    def name_exists(self, data, **kwargs):
        '''
        Validate the name exists and have a value
        
        :param self: Description
        :param data: Description
        :param kwargs: Description
        '''

        if not 'name' in data :
            raise ValidationError({'message':  gettext('nameRequired')})
        
        if not data['name']:
            raise ValidationError({'message':  gettext('nameRequired')})


class ListOut(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    distributors_ids = fields.List(fields.Integer, data_key='distributorsIds')
    users_ids = fields.List(fields.Integer, data_key='usersIds')
    slug = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class ListsOut(Schema):
    items = fields.List(fields.Nested(ListOut))
    total = fields.Integer()
