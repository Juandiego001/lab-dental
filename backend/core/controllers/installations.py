from core.services import installations
from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required
from core.schemas.utils import Message, Pagination
from core.schemas.installations import InstallationInUpdate, InstallationInCreate, InstallationOut, InstallationRejectCommentsIn, InstallationsOut


bp = APIBlueprint('installations', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(InstallationsOut)
@jwt_required()
def get_installations(query_data):
    '''Get installations'''

    try:
        results, total = installations.get_installations(query_data['search'],
                                                  query_data['page'],
                                                  query_data['per_page'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:installation_id>')
@bp.output(InstallationOut)
@jwt_required()
def get_installation(installation_id):
    '''Get installation'''

    try:
        return installations.get_installation_by_id(installation_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(InstallationInCreate, location='form_and_files')
@bp.output(Message)
@jwt_required()
def create_installations(form_and_files_data):
    '''Create installation'''

    try:
        installation = installations.create_installation(form_and_files_data)
        installations.notify_creation(installation)
        return {'message': 'Installation registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:installation_id>')
@bp.input(InstallationInUpdate, location='form_and_files')
@bp.output(Message)
@jwt_required()
def update_installations(installation_id, form_and_files_data):
    '''Update installation'''
    try:
        installations.update_installation(installation_id, form_and_files_data)
        return {'message': 'Installation updated successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:installation_id>')
@bp.output(Message)
@jwt_required()
def delete_installations(installation_id):
    '''Delete installations'''

    try:
        installations.delete_installation(installation_id)
        return {'message': 'Installation deleted successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.patch('/approve/<int:installation_id>')
@bp.output(Message)
@jwt_required()
def approve_installation(installation_id):
    '''Approve installation'''

    try:
        installations.approve_installation(installation_id)
        installations.notify_approval(installation_id)
        return {'message': 'Installation approved successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.post('/reject/<int:installation_id>')
@bp.input(InstallationRejectCommentsIn)
@bp.output(Message)
@jwt_required()
def reject_installation(installation_id, json_data):
    '''Reject installation'''

    try:
        print('JSON_DATA: ', json_data)
        installations.reject_installation(installation_id)
        installations.notify_rejection(installation_id, json_data['reject_comments'])
        return {'message': 'Installation rejected successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))