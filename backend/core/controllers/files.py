from flask import send_file
from core.schemas.files import PathIn
from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required
from flask_babel import gettext

bp = APIBlueprint('files', __name__)


@bp.get('/')
@bp.input(PathIn, location='query', arg_name='path')
@jwt_required()
def get_file(path):
    '''Get installations'''

    try:
        return send_file(path)
    except Exception as ex:
        abort(500, gettext('abortException'))
