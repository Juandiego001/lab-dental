import os
from apiflask.fields import String
from marshmallow import post_load
from core.schemas.utils import BaseSchema


class FileIn(BaseSchema):
  path = String()
  download = String(required=False, load_default='false')
  filename = String(required=False, load_default='')

  @post_load
  def set_real_file_path(self, data, **kwargs):
    '''Set real file path'''

    return os.path.join('../', data['path']), data['download'], data['filename']
