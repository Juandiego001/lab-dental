from flask_babel import gettext
from core.schemas.utils import Message
from core.services import installations
from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required, current_user
from core.schemas.installations import InstallationInUpdate, InstallationInCreate, InstallationOut, InstallationRejectCommentsIn, InstallationSearch, InstallationsOut


bp = APIBlueprint('installations', __name__)


@bp.post('/search')
@bp.input(InstallationSearch)
@bp.output(InstallationsOut)
@jwt_required()
def search_installations(json_data):
    '''Search installations'''

    try:
        results, total = installations.search_installations(
            current_user=current_user,
            equipment_id=json_data['equipment_id'],
            distributor_id=json_data['distributor_id'],
            client_id=json_data['client_id'],
            serial=json_data['serial'],
            status=json_data['status'],
            page=json_data['page'],
            per_page=json_data['per_page'],
            sort_by=json_data['sort_by'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:installation_id>')
@bp.output(InstallationOut)
@jwt_required()
def get_installation(installation_id):
    '''Get installation'''

    try:
        return installations.get_installation_by_id(installation_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/')
@bp.input(InstallationInCreate, location='form_and_files')
@bp.output(Message)
@jwt_required()
def create_installations(form_and_files_data):
    '''Create installation'''

    try:
        installation = installations.create_installation(
            current_user=current_user,
            data=form_and_files_data)
        installations.notify_creation(installation)
        return {'message': gettext('installationCreated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/<int:installation_id>')
@bp.input(InstallationInUpdate, location='form_and_files')
@bp.output(Message)
@jwt_required()
def update_installations(installation_id, form_and_files_data):
    '''Update installation'''
    try:
        installations.update_installation(installation_id, form_and_files_data)
        installations.notify_update(installation_id)
        return {'message': gettext('installationUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/<int:installation_id>')
@bp.output(Message)
@jwt_required()
def delete_installations(installation_id):
    '''Delete installations'''

    try:
        installations.delete_installation(installation_id)
        return {'message': gettext('installationDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.patch('/approve/<int:installation_id>')
@bp.output(Message)
@jwt_required()
def approve_installation(installation_id):
    '''Approve installation'''

    try:
        installations.approve_installation(installation_id)
        installations.notify_approval(installation_id)
        return {'message': gettext('installationApproved')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/reject/<int:installation_id>')
@bp.input(InstallationRejectCommentsIn)
@bp.output(Message)
@jwt_required()
def reject_installation(installation_id, json_data):
    '''Reject installation'''

    try:
        installations.reject_installation(installation_id)
        installations.notify_rejection(
            installation_id, json_data['reject_comments'])
        return {'message': gettext('installationRejected')}
    except Exception as ex:
        abort(500, gettext('abortException'))
