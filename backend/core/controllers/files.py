from flask import send_file
from core.schemas.files import FileIn
from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required
from flask_babel import gettext

bp = APIBlueprint('files', __name__)


@bp.get('/')
@bp.input(FileIn, location='query')
@jwt_required()
def get_file(query_data: str):
    '''Get installations'''

    try:
        path = query_data[0]
        download = query_data[1]
        filename = query_data[2]

        if download == 'true':
            if filename:
                return send_file(path, as_attachment=True, download_name=filename)
            else:
                return send_file(path, as_attachment=True)
        else:
            return send_file(path)
    except Exception as ex:
        print(ex)
        abort(500, gettext('abortException'))
