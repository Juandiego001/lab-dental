from apiflask import fields
from marshmallow import post_load
from core.models import Permission
from core.schemas.utils import BaseSchema


class PermissionIn(BaseSchema):
  id = fields.Integer()
  read = fields.Boolean()
  create = fields.Boolean()
  update = fields.Boolean()
  delete = fields.Boolean()

  @post_load
  def make_object(self, data, **kwargs):
    '''Make object permission'''

    return Permission(**data)


class PermissionGroupOut(BaseSchema):
  id = fields.Integer()
  read = fields.Boolean()
  create = fields.Boolean()
  update = fields.Boolean()
  delete = fields.Boolean()
  module_name = fields.String(data_key='moduleName')


class PermissionsGroupOut(BaseSchema):
  items = fields.List(fields.Nested(PermissionGroupOut))
  total = fields.Integer()