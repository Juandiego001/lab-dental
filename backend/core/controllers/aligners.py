from flask_babel import gettext
from core.schemas.utils import Message
from core.services import aligners
from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required
from core.schemas.aligners import AlignerOut, VersionOut
from werkzeug.exceptions import HTTPException


bp = APIBlueprint('aligners', __name__)


@bp.get('/<string:serial_number>')
@bp.output(AlignerOut)
@jwt_required()
def get_aligner(serial_number: str):
    '''Get aligners'''

    try:
        return aligners.get_aligner(
            serial_number=serial_number)
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/utils/version')
@bp.output(VersionOut)
@jwt_required()
def get_last_version():
    '''Get last version available'''

    try:
        return aligners.get_last_version()
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/stage/<string:serial_number>')
@bp.output(Message)
@jwt_required()
def send_stage_command(serial_number: str):
    '''Send stage command'''

    try:
        aligners.send_stage_command(
            serial_number=serial_number
        )
        return {'message': gettext('stageSuccess')}
    except Exception as ex:
        print(ex)
        abort(500, gettext('abortException'))


@bp.post('/unstage/<string:serial_number>')
@bp.output(Message)
@jwt_required()
def send_unstage_command(serial_number: str):
    '''Send unstage command'''

    try:
        aligners.send_unstage_command(
            serial_number=serial_number
        )
        return {'message': gettext('unstageSuccess')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/cloud/<string:serial_number>')
@bp.output(Message)
@jwt_required()
def send_cloud_command(serial_number: str):
    '''Send check cloud command'''

    try:
        aligners.send_cloud_command(
            serial_number=serial_number
        )
        return {'message': gettext('cloudSuccess')}
    except Exception as ex:
        abort(500, gettext('abortException'))
