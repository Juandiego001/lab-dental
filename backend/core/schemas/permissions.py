from core.schemas.utils import BaseSchema
from apiflask.fields import Integer, Boolean, String, List, Nested


class PermissionIn(BaseSchema):
    id = Integer()
    read = Boolean()
    create = Boolean()
    update = Boolean()
    delete = Boolean()


class PermissionGroupOut(BaseSchema):
    id = Integer()
    read = Boolean()
    create = Boolean()
    update = Boolean()
    delete = Boolean()
    module_name = String(data_key='moduleName')


class PermissionsGroupOut(BaseSchema):
    items = List(Nested(PermissionGroupOut))
    total = Integer()
