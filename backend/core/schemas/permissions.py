from apiflask import fields, Schema


class PermissionGroupOut(Schema):
  id = fields.Integer()
  read = fields.Boolean()
  create = fields.Boolean()
  update = fields.Boolean()
  delete = fields.Boolean()
  module_name = fields.String(data_key='moduleName')


class PermissionsGroupOut(Schema):
  items = fields.List(fields.Nested(PermissionGroupOut))
  total = fields.Integer()