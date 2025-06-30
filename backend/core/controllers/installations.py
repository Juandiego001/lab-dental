from flask_jwt_extended import get_jwt_identity, jwt_required
from core.services import installations
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.installations import InstallationInUpdate, InstallationInCreate, InstallationOut, InstallationsOut


bp = APIBlueprint('installations', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(InstallationsOut)
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
def get_installation(installation_id):
    '''Get installation'''

    try:
        return installations.get_installation_by_id(installation_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(InstallationInCreate, location='form_and_files')
def create_installations(form_and_files_data):
    '''Create installation'''

    try:
        installation = installations.create_installation(form_and_files_data)
        # installations.send_notification(1)
        return {'message': 'Installation registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:installation_id>')
@bp.input(InstallationInUpdate)
@bp.output(Message)
def update_installations(installation_id, json_data):
    '''Update installation'''
    try:
        installations.update_installation(installation_id, json_data)
        return {'message': 'Installation updated successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:installation_id>')
@bp.output(Message)
def delete_installations(installation_id):
    '''Delete installations'''

    try:
        installations.delete_installation(installation_id)
        return {'message': 'Installation deleted successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
