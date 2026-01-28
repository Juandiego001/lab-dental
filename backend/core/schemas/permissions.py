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