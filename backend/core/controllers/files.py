from flask import send_file
from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required
from flask_babel import gettext
from core.services import files


bp = APIBlueprint('files', __name__)


@bp.get('/users/<string:photo>')
@jwt_required()
def get_user_file(photo: str):
    '''Get user file'''

    try:
        user_file = files.get_user_file(photo)
        return send_file(
            user_file,
            as_attachment=False
        )
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/manuals/<string:hash_name>')
@jwt_required()
def get_manual_file(hash_name: str):
    '''Get manual file'''

    try:
        manual_file, mimetype = files.get_manual_file(hash_name)
        return send_file(
            manual_file,
            mimetype=mimetype,
            as_attachment=False
        )
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/equipments/<string:hash_name>')
@jwt_required()
def get_equipment_file(hash_name: str):
    '''Get equipment file'''

    try:
        equipment_file, mimetype = files.get_equipment_file(hash_name)
        return send_file(
            equipment_file,
            mimetype=mimetype,
            as_attachment=False
        )
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/installations/<string:hash_name>')
@jwt_required()
def get_installation_file(hash_name: str):
    '''Get installation file'''

    try:
        installation_file, mimetype = files.get_installation_file(hash_name)
        return send_file(
            installation_file,
            mimetype=mimetype,
            as_attachment=False
        )
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/warranties/<string:hash_name>')
@jwt_required()
def get_warranty_file(hash_name: str):
    '''Get warranty file'''

    try:
        warranty_file, mimetype = files.get_warranty_file(hash_name)
        return send_file(
            warranty_file,
            mimetype=mimetype,
            as_attachment=False
        )
    except Exception as ex:
        abort(500, gettext('abortException'))
