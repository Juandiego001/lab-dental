import os
from apiflask import fields
from marshmallow import post_load
from core.schemas.utils import BaseSchema


class PathIn(BaseSchema):
  path = fields.String()

  @post_load
  def set_real_file_path(self, data, **kwargs):
    '''Set real file path'''

    return os.path.join('../', data['path'])
